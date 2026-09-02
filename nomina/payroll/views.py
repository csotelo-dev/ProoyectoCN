"""Vistas del módulo Payroll — Gestión de nómina."""

from core.models import RegistroAuditoria
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import NovedadForm, ParametroNominaForm, PeriodoNominaForm
from .models import Nomina, Novedad, ParametroNomina, PeriodoNomina
from .services import liquidar_periodo_completo


class ParametroNominaListView(LoginRequiredMixin, ListView):
    model = ParametroNomina
    template_name = "payroll/parametro_list.html"
    context_object_name = "parametros"


class ParametroNominaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ParametroNomina
    form_class = ParametroNominaForm
    template_name = "payroll/parametro_form.html"
    success_url = reverse_lazy("parametro-list")
    permission_required = "payroll.add_parametronomina"


class PeriodoNominaListView(LoginRequiredMixin, ListView):
    model = PeriodoNomina
    template_name = "payroll/periodo_list.html"
    context_object_name = "periodos"


class PeriodoNominaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PeriodoNomina
    form_class = PeriodoNominaForm
    template_name = "payroll/periodo_form.html"
    success_url = reverse_lazy("periodo-list")
    permission_required = "payroll.add_periodonomina"

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class PeriodoNominaDetailView(LoginRequiredMixin, DetailView):
    model = PeriodoNomina
    template_name = "payroll/periodo_detail.html"
    context_object_name = "periodo"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["nominas"] = self.object.nominas.select_related(
            "contrato__empleado", "contrato__cargo"
        ).all()
        ctx["novedades"] = self.object.novedades.select_related("empleado").all()
        return ctx


@login_required
@permission_required("payroll.change_periodonomina", raise_exception=True)
def liquidar_periodo(request, pk):
    """Ejecuta la liquidación completa de un periodo de nómina."""
    periodo = get_object_or_404(PeriodoNomina, pk=pk)

    if periodo.estado not in ("BORRADOR", "LIQUIDADO"):
        messages.error(request, "Solo se pueden liquidar periodos en estado Borrador o Liquidado.")
        return redirect("periodo-detail", pk=pk)

    nominas = liquidar_periodo_completo(periodo, usuario=request.user)

    RegistroAuditoria.objects.create(
        usuario=request.user,
        accion="LIQUIDAR",
        modelo="PeriodoNomina",
        objeto_id=str(pk),
        detalle=f"Liquidación del periodo {periodo.nombre} — {len(nominas)} nóminas procesadas",
        ip_address=request.META.get("REMOTE_ADDR"),
    )

    messages.success(request, f"Periodo liquidado exitosamente. {len(nominas)} nóminas procesadas.")
    return redirect("periodo-detail", pk=pk)


class NovedadCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Novedad
    form_class = NovedadForm
    template_name = "payroll/novedad_form.html"
    permission_required = "payroll.add_novedad"

    def get_success_url(self):
        return reverse_lazy("periodo-detail", kwargs={"pk": self.object.periodo.pk})

    def get_initial(self):
        initial = super().get_initial()
        periodo_pk = self.kwargs.get("periodo_pk")
        if periodo_pk:
            initial["periodo"] = periodo_pk
        return initial


class NominaDetailView(LoginRequiredMixin, DetailView):
    model = Nomina
    template_name = "payroll/nomina_detail.html"
    context_object_name = "nomina"
