"""
Motor de liquidación de nómina colombiana.

Calcula devengados, deducciones y aportes según la legislación laboral
colombiana vigente. Cada cálculo es determinista y auditable.
"""

from decimal import ROUND_HALF_UP, Decimal

from core.models import Contrato
from django.utils import timezone

from .models import Nomina, Novedad, PeriodoNomina

# Factores de recargo para horas extra (Código Sustantivo del Trabajo)
FACTOR_HORA_EXTRA = {
    "HE_DIURNA": Decimal("1.25"),
    "HE_NOCTURNA": Decimal("1.75"),
    "HE_DOM_DIURNA": Decimal("2.00"),
    "HE_DOM_NOCTURNA": Decimal("2.50"),
}

TIPOS_HORA_EXTRA = set(FACTOR_HORA_EXTRA.keys())
TIPOS_DEDUCCION = {"DEDUCCION", "PRESTAMO", "LIBRANZA"}
TIPOS_BONIFICACION = {"BONIFICACION", "COMISION"}


def _round2(value: Decimal) -> Decimal:
    """Redondea a 2 decimales con criterio bancario."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calcular_valor_hora(salario_mensual: Decimal) -> Decimal:
    """Salario mensual / 240 horas (jornada legal colombiana)."""
    return _round2(salario_mensual / Decimal("240"))


def liquidar_nomina_empleado(periodo: PeriodoNomina, contrato: Contrato, usuario=None) -> Nomina:
    """
    Liquida la nómina de un contrato para un periodo dado.

    Pasos:
    1. Calcular salario proporcional a días trabajados.
    2. Determinar si aplica auxilio de transporte.
    3. Sumar novedades (horas extra, bonificaciones, deducciones).
    4. Calcular aportes a seguridad social.
    5. Calcular neto a pagar.
    """
    params = periodo.parametros
    dias = 30  # Nómina mensual estándar Colombia

    # 1. Salario proporcional
    salario_base = _round2(contrato.salario_base * Decimal(dias) / Decimal("30"))

    # 2. Auxilio de transporte (si salario <= tope SMMLV)
    tope_auxilio = params.smmlv * params.tope_auxilio_transporte_smmlv
    if contrato.auxilio_transporte and contrato.salario_base <= tope_auxilio:
        auxilio_transporte = _round2(params.auxilio_transporte * Decimal(dias) / Decimal("30"))
    else:
        auxilio_transporte = Decimal("0")

    # 3. Novedades del periodo para este empleado
    novedades = Novedad.objects.filter(periodo=periodo, empleado=contrato.empleado)

    valor_hora = calcular_valor_hora(contrato.salario_base)
    total_horas_extra = Decimal("0")
    total_bonificaciones = Decimal("0")
    total_comisiones = Decimal("0")
    total_otras_deducciones = Decimal("0")

    for nov in novedades:
        if nov.tipo in TIPOS_HORA_EXTRA:
            factor = FACTOR_HORA_EXTRA[nov.tipo]
            total_horas_extra += _round2(nov.cantidad * valor_hora * factor)
        elif nov.tipo == "BONIFICACION":
            total_bonificaciones += nov.valor
        elif nov.tipo == "COMISION":
            total_comisiones += nov.valor
        elif nov.tipo in TIPOS_DEDUCCION:
            total_otras_deducciones += nov.valor

    # Total devengado (incluye auxilio de transporte)
    total_devengado = salario_base + auxilio_transporte + total_horas_extra + total_bonificaciones + total_comisiones

    # 4. Base para seguridad social (NO incluye auxilio de transporte)
    ibc = salario_base + total_horas_extra + total_bonificaciones + total_comisiones

    # Aportes del empleado
    aporte_salud_empleado = _round2(ibc * params.porcentaje_salud_empleado / Decimal("100"))
    aporte_pension_empleado = _round2(ibc * params.porcentaje_pension_empleado / Decimal("100"))

    # Aportes del empleador (informativos)
    aporte_salud_empleador = _round2(ibc * params.porcentaje_salud_empleador / Decimal("100"))
    aporte_pension_empleador = _round2(ibc * params.porcentaje_pension_empleador / Decimal("100"))
    aporte_arl = _round2(ibc * params.porcentaje_arl_base / Decimal("100"))
    aporte_sena = _round2(ibc * params.porcentaje_sena / Decimal("100"))
    aporte_icbf = _round2(ibc * params.porcentaje_icbf / Decimal("100"))
    aporte_caja = _round2(ibc * params.porcentaje_caja_compensacion / Decimal("100"))

    # 5. Total deducciones y neto
    total_deducciones = aporte_salud_empleado + aporte_pension_empleado + total_otras_deducciones
    neto_pagar = total_devengado - total_deducciones

    # Crear o actualizar registro de nómina
    nomina, _ = Nomina.objects.update_or_create(
        periodo=periodo,
        contrato=contrato,
        defaults={
            "dias_trabajados": dias,
            "salario_base": salario_base,
            "auxilio_transporte": auxilio_transporte,
            "total_horas_extra": total_horas_extra,
            "total_bonificaciones": total_bonificaciones,
            "total_comisiones": total_comisiones,
            "total_devengado": total_devengado,
            "aporte_salud_empleado": aporte_salud_empleado,
            "aporte_pension_empleado": aporte_pension_empleado,
            "total_otras_deducciones": total_otras_deducciones,
            "total_deducciones": total_deducciones,
            "aporte_salud_empleador": aporte_salud_empleador,
            "aporte_pension_empleador": aporte_pension_empleador,
            "aporte_arl": aporte_arl,
            "aporte_sena": aporte_sena,
            "aporte_icbf": aporte_icbf,
            "aporte_caja_compensacion": aporte_caja,
            "neto_pagar": neto_pagar,
            "liquidado_en": timezone.now(),
            "liquidado_por": usuario,
        },
    )
    return nomina


def liquidar_periodo_completo(periodo: PeriodoNomina, usuario=None) -> list[Nomina]:
    """Liquida la nómina de todos los contratos activos para un periodo."""
    contratos_activos = Contrato.objects.filter(
        activo=True,
        fecha_inicio__lte=periodo.fecha_fin,
    ).select_related("empleado", "cargo")

    resultados = []
    for contrato in contratos_activos:
        if contrato.fecha_fin and contrato.fecha_fin < periodo.fecha_inicio:
            continue
        nomina = liquidar_nomina_empleado(periodo, contrato, usuario)
        resultados.append(nomina)

    periodo.estado = "LIQUIDADO"
    periodo.save(update_fields=["estado"])
    return resultados
