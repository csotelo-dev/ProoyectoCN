"""Configuración del panel de administración — módulo Core."""

from django.contrib import admin

from .models import Cargo, Contrato, Departamento, Empleado, RegistroAuditoria


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo", "creado_en")
    list_filter = ("activo",)
    search_fields = ("nombre",)


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "departamento", "nivel_riesgo_arl", "activo")
    list_filter = ("departamento", "activo", "nivel_riesgo_arl")
    search_fields = ("nombre",)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        "numero_documento",
        "primer_nombre",
        "primer_apellido",
        "eps",
        "activo",
    )
    list_filter = ("activo", "tipo_documento")
    search_fields = ("numero_documento", "primer_nombre", "primer_apellido")
    readonly_fields = ("creado_en", "actualizado_en")


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = (
        "empleado",
        "cargo",
        "tipo_contrato",
        "salario_base",
        "fecha_inicio",
        "activo",
    )
    list_filter = ("tipo_contrato", "activo")
    search_fields = ("empleado__primer_nombre", "empleado__numero_documento")
    readonly_fields = ("creado_en",)


@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "usuario", "accion", "modelo", "objeto_id")
    list_filter = ("accion", "modelo")
    search_fields = ("usuario__username", "detalle")
    readonly_fields = (
        "usuario",
        "accion",
        "modelo",
        "objeto_id",
        "detalle",
        "ip_address",
        "timestamp",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
