"""Configuración del panel de administración — módulo Payroll."""

from django.contrib import admin

from .models import Nomina, Novedad, ParametroNomina, PeriodoNomina


@admin.register(ParametroNomina)
class ParametroNominaAdmin(admin.ModelAdmin):
    list_display = ("anio", "smmlv", "auxilio_transporte")


@admin.register(PeriodoNomina)
class PeriodoNominaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "fecha_inicio", "fecha_fin", "estado", "creado_por")
    list_filter = ("estado",)


@admin.register(Novedad)
class NovedadAdmin(admin.ModelAdmin):
    list_display = ("periodo", "empleado", "tipo", "cantidad", "valor")
    list_filter = ("tipo", "periodo")
    search_fields = ("empleado__primer_nombre", "empleado__numero_documento")


@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = (
        "contrato",
        "periodo",
        "salario_base",
        "total_devengado",
        "total_deducciones",
        "neto_pagar",
    )
    list_filter = ("periodo",)
    readonly_fields = (
        "salario_base",
        "auxilio_transporte",
        "total_horas_extra",
        "total_bonificaciones",
        "total_comisiones",
        "total_devengado",
        "aporte_salud_empleado",
        "aporte_pension_empleado",
        "total_otras_deducciones",
        "total_deducciones",
        "aporte_salud_empleador",
        "aporte_pension_empleador",
        "aporte_arl",
        "aporte_sena",
        "aporte_icbf",
        "aporte_caja_compensacion",
        "neto_pagar",
        "liquidado_en",
        "liquidado_por",
    )
