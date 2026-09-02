"""Vistas API REST — Canal de autoconsulta para empleados."""

from core.models import Cargo, Contrato, Departamento, Empleado
from payroll.models import Nomina, PeriodoNomina
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    CargoSerializer,
    ContratoSerializer,
    DepartamentoSerializer,
    EmpleadoSerializer,
    NominaSerializer,
    PeriodoNominaSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permiso: lectura para autenticados, escritura solo para staff."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_staff


class DepartamentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Departamento.objects.filter(activo=True)
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CargoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cargo.objects.filter(activo=True).select_related("departamento")
    serializer_class = CargoSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmpleadoViewSet(viewsets.ModelViewSet):
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["activo", "tipo_documento"]
    search_fields = ["primer_nombre", "primer_apellido", "numero_documento"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Empleado.objects.all()
        # Empleados solo ven su propio perfil
        return Empleado.objects.filter(usuario=user)


class ContratoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContratoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Contrato.objects.select_related("empleado", "cargo")
        if user.is_staff:
            return qs.all()
        return qs.filter(empleado__usuario=user)


class PeriodoNominaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PeriodoNomina.objects.all()
    serializer_class = PeriodoNominaSerializer
    permission_classes = [permissions.IsAuthenticated]


class NominaViewSet(viewsets.ReadOnlyModelViewSet):
    """Desprendibles de nómina — empleados solo ven los propios."""

    serializer_class = NominaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["periodo"]

    def get_queryset(self):
        user = self.request.user
        qs = Nomina.objects.select_related(
            "contrato__empleado", "contrato__cargo", "periodo"
        )
        if user.is_staff:
            return qs.all()
        return qs.filter(contrato__empleado__usuario=user)

    @action(detail=False, methods=["get"])
    def mi_ultimo_desprendible(self, request):
        """Endpoint de autoconsulta: último desprendible del empleado autenticado."""
        nomina = (
            Nomina.objects.filter(contrato__empleado__usuario=request.user)
            .select_related("contrato__empleado", "periodo")
            .order_by("-periodo__fecha_fin")
            .first()
        )
        if nomina is None:
            return Response({"detail": "No tiene desprendibles disponibles."}, status=404)
        serializer = self.get_serializer(nomina)
        return Response(serializer.data)
