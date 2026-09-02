"""Vistas del módulo Core — CRUD de empleados, departamentos, cargos, contratos."""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import models
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from payroll.models import Nomina, PeriodoNomina

from .forms import CargoForm, ContratoForm, DepartamentoForm, EmpleadoForm
from .models import Cargo, Contrato, Departamento, Empleado

# --- Dashboard ---------------------------------------------------------------

@login_required
def dashboard(request):
    """Vista principal con resumen del sistema."""
    contratos_activos = Contrato.objects.filter(activo=True).select_related("empleado", "cargo")
    ultimo_periodo = PeriodoNomina.objects.order_by("-fecha_fin").first()

    # Totales de nomina del ultimo periodo
    total_nomina_neto = None
    total_nomina_devengado = None
    nominas_count = 0
    if ultimo_periodo:
        agg = Nomina.objects.filter(periodo=ultimo_periodo).aggregate(
            neto=Sum("neto_pagar"),
            devengado=Sum("total_devengado"),
        )
        total_nomina_neto = agg["neto"]
        total_nomina_devengado = agg["devengado"]
        nominas_count = Nomina.objects.filter(periodo=ultimo_periodo).count()

    # Distribucion por departamento
    departamentos_con_empleados = []
    for dep in Departamento.objects.filter(activo=True).order_by("nombre"):
        count = Contrato.objects.filter(cargo__departamento=dep, activo=True).count()
        if count > 0:
            departamentos_con_empleados.append({"nombre": dep.nombre, "count": count})

    context = {
        "total_empleados": Empleado.objects.filter(activo=True).count(),
        "total_departamentos": Departamento.objects.filter(activo=True).count(),
        "total_contratos": contratos_activos.count(),
        "total_cargos": Cargo.objects.filter(activo=True).count(),
        "empleados_recientes": Empleado.objects.filter(activo=True).order_by("-creado_en")[:5],
        "contratos_recientes": contratos_activos.order_by("-creado_en")[:5],
        "ultimo_periodo": ultimo_periodo,
        "total_nomina_neto": total_nomina_neto,
        "total_nomina_devengado": total_nomina_devengado,
        "nominas_count": nominas_count,
        "departamentos_con_empleados": departamentos_con_empleados,
        "periodos_pendientes": PeriodoNomina.objects.filter(estado="BORRADOR").count(),
    }
    return render(request, "core/dashboard.html", context)


# --- Departamentos -----------------------------------------------------------

class DepartamentoListView(LoginRequiredMixin, ListView):
    model = Departamento
    template_name = "core/departamento_list.html"
    context_object_name = "departamentos"
    paginate_by = 20


class DepartamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = "core/departamento_form.html"
    success_url = reverse_lazy("departamento-list")
    permission_required = "core.add_departamento"


class DepartamentoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = "core/departamento_form.html"
    success_url = reverse_lazy("departamento-list")
    permission_required = "core.change_departamento"


class DepartamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Departamento
    template_name = "core/departamento_confirm_delete.html"
    success_url = reverse_lazy("departamento-list")
    permission_required = "core.delete_departamento"


# --- Cargos ------------------------------------------------------------------

class CargoListView(LoginRequiredMixin, ListView):
    model = Cargo
    template_name = "core/cargo_list.html"
    context_object_name = "cargos"
    paginate_by = 20


class CargoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = "core/cargo_form.html"
    success_url = reverse_lazy("cargo-list")
    permission_required = "core.add_cargo"


class CargoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = "core/cargo_form.html"
    success_url = reverse_lazy("cargo-list")
    permission_required = "core.change_cargo"


# --- Empleados ---------------------------------------------------------------

class EmpleadoListView(LoginRequiredMixin, ListView):
    model = Empleado
    template_name = "core/empleado_list.html"
    context_object_name = "empleados"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                models.Q(primer_nombre__icontains=q)
                | models.Q(primer_apellido__icontains=q)
                | models.Q(numero_documento__icontains=q)
            )
        return qs


class EmpleadoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = "core/empleado_form.html"
    success_url = reverse_lazy("empleado-list")
    permission_required = "core.add_empleado"


class EmpleadoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = "core/empleado_form.html"
    success_url = reverse_lazy("empleado-list")
    permission_required = "core.change_empleado"


class EmpleadoDetailView(LoginRequiredMixin, DetailView):
    model = Empleado
    template_name = "core/empleado_detail.html"
    context_object_name = "empleado"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["contratos"] = self.object.contratos.all()
        return ctx


# --- Contratos ---------------------------------------------------------------

class ContratoListView(LoginRequiredMixin, ListView):
    model = Contrato
    template_name = "core/contrato_list.html"
    context_object_name = "contratos"
    paginate_by = 20


class ContratoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Contrato
    form_class = ContratoForm
    template_name = "core/contrato_form.html"
    success_url = reverse_lazy("contrato-list")
    permission_required = "core.add_contrato"


class ContratoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Contrato
    form_class = ContratoForm
    template_name = "core/contrato_form.html"
    success_url = reverse_lazy("contrato-list")
    permission_required = "core.change_contrato"
