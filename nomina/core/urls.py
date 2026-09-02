"""URLs del módulo Core."""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    # Autenticación
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(http_method_names=["get", "post", "options"]), name="logout"),
    # Departamentos
    path("departamentos/", views.DepartamentoListView.as_view(), name="departamento-list"),
    path("departamentos/crear/", views.DepartamentoCreateView.as_view(), name="departamento-create"),
    path("departamentos/<int:pk>/editar/", views.DepartamentoUpdateView.as_view(), name="departamento-update"),
    path("departamentos/<int:pk>/eliminar/", views.DepartamentoDeleteView.as_view(), name="departamento-delete"),
    # Cargos
    path("cargos/", views.CargoListView.as_view(), name="cargo-list"),
    path("cargos/crear/", views.CargoCreateView.as_view(), name="cargo-create"),
    path("cargos/<int:pk>/editar/", views.CargoUpdateView.as_view(), name="cargo-update"),
    # Empleados
    path("empleados/", views.EmpleadoListView.as_view(), name="empleado-list"),
    path("empleados/crear/", views.EmpleadoCreateView.as_view(), name="empleado-create"),
    path("empleados/<int:pk>/", views.EmpleadoDetailView.as_view(), name="empleado-detail"),
    path("empleados/<int:pk>/editar/", views.EmpleadoUpdateView.as_view(), name="empleado-update"),
    # Contratos
    path("contratos/", views.ContratoListView.as_view(), name="contrato-list"),
    path("contratos/crear/", views.ContratoCreateView.as_view(), name="contrato-create"),
    path("contratos/<int:pk>/editar/", views.ContratoUpdateView.as_view(), name="contrato-update"),
]
