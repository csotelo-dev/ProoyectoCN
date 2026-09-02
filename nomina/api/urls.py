"""URLs de la API REST."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"departamentos", views.DepartamentoViewSet)
router.register(r"cargos", views.CargoViewSet)
router.register(r"empleados", views.EmpleadoViewSet, basename="empleado")
router.register(r"contratos", views.ContratoViewSet, basename="contrato")
router.register(r"periodos", views.PeriodoNominaViewSet)
router.register(r"nominas", views.NominaViewSet, basename="nomina")

urlpatterns = [
    path("", include(router.urls)),
]
