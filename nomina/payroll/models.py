"""
Modelos del módulo Payroll — Liquidación de Nómina.

Implementa el cálculo de nómina mensual colombiana con:
- Salario base, auxilio de transporte
- Novedades (horas extra, incapacidades, vacaciones, bonificaciones, deducciones)
- Aportes a seguridad social (salud, pensión, ARL)
- Aportes parafiscales (SENA, ICBF, Caja de Compensación)
"""

from decimal import Decimal

from core.models import Contrato, Empleado
from django.conf import settings
from django.db import models


class ParametroNomina(models.Model):
    """Parámetros legales de nómina vigentes para un año fiscal."""

    anio = models.PositiveIntegerField(unique=True, verbose_name="Año")
    smmlv = models.DecimalField(
        "SMMLV", max_digits=12, decimal_places=2, help_text="Salario minimo mensual legal vigente",
    )
    auxilio_transporte = models.DecimalField(max_digits=12, decimal_places=2)
    tope_auxilio_transporte_smmlv = models.PositiveSmallIntegerField(
        default=2, help_text="Aplica si salario <= N SMMLV",
    )
    porcentaje_salud_empleado = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("4.00"))
    porcentaje_salud_empleador = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("8.50"))
    porcentaje_pension_empleado = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("4.00"))
    porcentaje_pension_empleador = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("12.00"))
    porcentaje_arl_base = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal("0.5220"))
    porcentaje_sena = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("2.00"))
    porcentaje_icbf = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("3.00"))
    porcentaje_caja_compensacion = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("4.00"))

    class Meta:
        ordering = ["-anio"]
        verbose_name = "parámetro de nómina"
        verbose_name_plural = "parámetros de nómina"

    def __str__(self):
        return f"Parámetros {self.anio} — SMMLV: ${self.smmlv:,.0f}"


class PeriodoNomina(models.Model):
    """Periodo de liquidación (mensual)."""

    ESTADO_CHOICES = [
        ("BORRADOR", "Borrador"),
        ("LIQUIDADO", "Liquidado"),
        ("APROBADO", "Aprobado"),
        ("PAGADO", "Pagado"),
    ]

    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default="BORRADOR")
    parametros = models.ForeignKey(ParametroNomina, on_delete=models.PROTECT)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_inicio"]
        verbose_name = "período de nómina"
        verbose_name_plural = "períodos de nómina"

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"


class Novedad(models.Model):
    """Novedades que afectan la liquidación de un empleado en un periodo."""

    TIPO_CHOICES = [
        ("HE_DIURNA", "Hora Extra Diurna (25%)"),
        ("HE_NOCTURNA", "Hora Extra Nocturna (75%)"),
        ("HE_DOM_DIURNA", "Hora Extra Dominical Diurna (100%)"),
        ("HE_DOM_NOCTURNA", "Hora Extra Dominical Nocturna (150%)"),
        ("INCAPACIDAD", "Incapacidad"),
        ("VACACIONES", "Vacaciones"),
        ("LICENCIA", "Licencia"),
        ("BONIFICACION", "Bonificación"),
        ("COMISION", "Comisión"),
        ("DEDUCCION", "Deducción"),
        ("PRESTAMO", "Descuento por Préstamo"),
        ("LIBRANZA", "Descuento por Libranza"),
    ]

    periodo = models.ForeignKey(PeriodoNomina, on_delete=models.CASCADE, related_name="novedades")
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name="novedades")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
        help_text="Horas, días o unidades según el tipo",
    )
    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0"),
        help_text="Valor fijo (para bonificaciones, deducciones, etc.)",
    )
    observacion = models.TextField(blank=True)

    class Meta:
        verbose_name = "novedad"
        verbose_name_plural = "novedades"

    def __str__(self):
        return f"{self.empleado} — {self.get_tipo_display()} — {self.periodo}"


class Nomina(models.Model):
    """Liquidación individual de nómina de un empleado en un periodo."""

    periodo = models.ForeignKey(PeriodoNomina, on_delete=models.CASCADE, related_name="nominas")
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name="nominas")
    dias_trabajados = models.PositiveSmallIntegerField(default=30)

    # Devengados
    salario_base = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    auxilio_transporte = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    total_horas_extra = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    total_bonificaciones = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    total_comisiones = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    total_devengado = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))

    # Deducciones del empleado
    aporte_salud_empleado = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    aporte_pension_empleado = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    total_otras_deducciones = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    total_deducciones = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))

    # Aportes del empleador (informativos)
    aporte_salud_empleador = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    aporte_pension_empleador = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    aporte_arl = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    aporte_sena = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    aporte_icbf = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    aporte_caja_compensacion = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))

    # Neto a pagar
    neto_pagar = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))

    liquidado_en = models.DateTimeField(null=True, blank=True)
    liquidado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        unique_together = ["periodo", "contrato"]
        ordering = ["contrato__empleado__primer_apellido"]
        verbose_name = "nómina"
        verbose_name_plural = "nóminas"

    def __str__(self):
        return f"{self.contrato.empleado} — {self.periodo} — Neto: ${self.neto_pagar:,.0f}"
