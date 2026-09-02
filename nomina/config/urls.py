"""URL configuration — Sistema de Gestión de Talento Humano y Nómina."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("nomina/", include("payroll.urls")),
    path("", include("core.urls")),
]
