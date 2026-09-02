"""URLs del módulo Payroll."""

from django.urls import path

from . import views

urlpatterns = [
    # Parámetros de nómina
    path("parametros/", views.ParametroNominaListView.as_view(), name="parametro-list"),
    path("parametros/crear/", views.ParametroNominaCreateView.as_view(), name="parametro-create"),
    # Periodos de nómina
    path("periodos/", views.PeriodoNominaListView.as_view(), name="periodo-list"),
    path("periodos/crear/", views.PeriodoNominaCreateView.as_view(), name="periodo-create"),
    path("periodos/<int:pk>/", views.PeriodoNominaDetailView.as_view(), name="periodo-detail"),
    path("periodos/<int:pk>/liquidar/", views.liquidar_periodo, name="periodo-liquidar"),
    # Novedades
    path("novedades/crear/", views.NovedadCreateView.as_view(), name="novedad-create"),
    path("novedades/crear/<int:periodo_pk>/", views.NovedadCreateView.as_view(), name="novedad-create-periodo"),
    # Desprendible individual
    path("desprendible/<int:pk>/", views.NominaDetailView.as_view(), name="nomina-detail"),
]
