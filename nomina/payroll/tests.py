"""
Tests del módulo Payroll — Motor de Liquidación de Nómina.

Verifica la exactitud de los cálculos de nómina colombiana.
Objetivo: >= 99% de exactitud (ISO/IEC 25010 — exactitud funcional).
"""

from decimal import Decimal

import pytest

from payroll.models import Nomina, Novedad
from payroll.services import (
    _round2,
    calcular_valor_hora,
    liquidar_nomina_empleado,
    liquidar_periodo_completo,
)


@pytest.mark.django_db
class TestCalculosSalario:
    """Tests de cálculos individuales de nómina."""

    def test_valor_hora(self):
        """Salario / 240 horas (jornada legal colombiana)."""
        salario = Decimal("1300000")
        esperado = Decimal("5416.67")
        assert calcular_valor_hora(salario) == esperado

    def test_round2(self):
        assert _round2(Decimal("1234.5678")) == Decimal("1234.57")
        assert _round2(Decimal("1234.5650")) == Decimal("1234.57")


@pytest.mark.django_db
class TestLiquidacionNomina:
    """Tests de liquidación completa de un empleado."""

    def test_liquidar_salario_minimo_con_auxilio(self, periodo, contrato, admin_user):
        """Empleado con salario <= 2 SMMLV debe recibir auxilio de transporte."""
        contrato.salario_base = Decimal("1300000")
        contrato.auxilio_transporte = True
        contrato.save()

        nomina = liquidar_nomina_empleado(periodo, contrato, admin_user)

        assert nomina.salario_base == Decimal("1300000.00")
        assert nomina.auxilio_transporte == Decimal("200000.00")
        # Salud empleado: 1300000 * 4% = 52000
        assert nomina.aporte_salud_empleado == Decimal("52000.00")
        # Pensión empleado: 1300000 * 4% = 52000
        assert nomina.aporte_pension_empleado == Decimal("52000.00")
        # Devengado = 1300000 + 200000 = 1500000
        assert nomina.total_devengado == Decimal("1500000.00")
        # Deducciones = 52000 + 52000 = 104000
        assert nomina.total_deducciones == Decimal("104000.00")
        # Neto = 1500000 - 104000 = 1396000
        assert nomina.neto_pagar == Decimal("1396000.00")

    def test_liquidar_salario_alto_sin_auxilio(self, periodo, contrato, admin_user):
        """Empleado con salario > 2 SMMLV NO recibe auxilio de transporte."""
        contrato.salario_base = Decimal("5000000")
        contrato.auxilio_transporte = True
        contrato.save()

        nomina = liquidar_nomina_empleado(periodo, contrato, admin_user)

        assert nomina.auxilio_transporte == Decimal("0")
        assert nomina.salario_base == Decimal("5000000.00")

    def test_liquidar_con_horas_extra_diurnas(self, periodo, contrato, admin_user, empleado):
        """Horas extra diurnas se calculan con factor 1.25."""
        contrato.salario_base = Decimal("1300000")
        contrato.save()

        Novedad.objects.create(
            periodo=periodo,
            empleado=empleado,
            tipo="HE_DIURNA",
            cantidad=Decimal("10"),
        )

        nomina = liquidar_nomina_empleado(periodo, contrato, admin_user)

        # Valor hora = 1300000 / 240 = 5416.67
        # HE diurna = 10 * 5416.67 * 1.25 = 67708.38
        assert nomina.total_horas_extra == Decimal("67708.38")

    def test_liquidar_con_bonificacion(self, periodo, contrato, admin_user, empleado):
        """Las bonificaciones se suman al devengado y afectan la base de seguridad social."""
        contrato.salario_base = Decimal("1300000")
        contrato.save()

        Novedad.objects.create(
            periodo=periodo,
            empleado=empleado,
            tipo="BONIFICACION",
            valor=Decimal("200000"),
        )

        nomina = liquidar_nomina_empleado(periodo, contrato, admin_user)

        assert nomina.total_bonificaciones == Decimal("200000")
        # IBC incluye la bonificación: 1300000 + 200000 = 1500000
        assert nomina.aporte_salud_empleado == Decimal("60000.00")  # 1500000 * 4%

    def test_liquidar_con_deduccion(self, periodo, contrato, admin_user, empleado):
        """Las deducciones se restan del neto a pagar."""
        contrato.salario_base = Decimal("1300000")
        contrato.save()

        Novedad.objects.create(
            periodo=periodo,
            empleado=empleado,
            tipo="DEDUCCION",
            valor=Decimal("50000"),
            observacion="Descuento por uniforme",
        )

        nomina = liquidar_nomina_empleado(periodo, contrato, admin_user)

        assert nomina.total_otras_deducciones == Decimal("50000")
        assert nomina.neto_pagar == Decimal("1346000.00")  # 1396000 - 50000

    def test_aportes_empleador(self, periodo, contrato, admin_user):
        """Verificar cálculo de aportes patronales."""
        contrato.salario_base = Decimal("1300000")
        contrato.save()

        nomina = liquidar_nomina_empleado(periodo, contrato, admin_user)

        # Salud empleador: 1300000 * 8.50% = 110500
        assert nomina.aporte_salud_empleador == Decimal("110500.00")
        # Pensión empleador: 1300000 * 12% = 156000
        assert nomina.aporte_pension_empleador == Decimal("156000.00")
        # ARL: 1300000 * 0.522% = 6786.00
        assert nomina.aporte_arl == Decimal("6786.00")
        # SENA: 1300000 * 2% = 26000
        assert nomina.aporte_sena == Decimal("26000.00")
        # ICBF: 1300000 * 3% = 39000
        assert nomina.aporte_icbf == Decimal("39000.00")
        # Caja: 1300000 * 4% = 52000
        assert nomina.aporte_caja_compensacion == Decimal("52000.00")


@pytest.mark.django_db
class TestLiquidacionPeriodo:
    """Tests de liquidación masiva de un periodo."""

    def test_liquidar_periodo_completo(self, periodo, contrato, admin_user):
        """Liquidar un periodo genera nóminas para todos los contratos activos."""
        nominas = liquidar_periodo_completo(periodo, admin_user)

        assert len(nominas) == 1
        periodo.refresh_from_db()
        assert periodo.estado == "LIQUIDADO"

    def test_no_duplicar_nomina_en_reliquidacion(self, periodo, contrato, admin_user):
        """Reliquidar un periodo actualiza las nóminas existentes, no las duplica."""
        liquidar_periodo_completo(periodo, admin_user)
        liquidar_periodo_completo(periodo, admin_user)

        assert Nomina.objects.filter(periodo=periodo).count() == 1

    def test_contrato_inactivo_no_se_liquida(self, periodo, contrato, admin_user):
        """Contratos inactivos no se incluyen en la liquidación."""
        contrato.activo = False
        contrato.save()

        nominas = liquidar_periodo_completo(periodo, admin_user)
        assert len(nominas) == 0
