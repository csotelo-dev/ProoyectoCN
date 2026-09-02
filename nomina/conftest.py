"""Fixtures compartidas para pruebas con pytest-django."""

from datetime import date
from decimal import Decimal

import pytest
from core.models import Cargo, Contrato, Departamento, Empleado
from django.contrib.auth.models import User
from payroll.models import ParametroNomina, PeriodoNomina


@pytest.fixture
def admin_user(db):
    """Usuario administrador para pruebas."""
    return User.objects.create_superuser(
        username="admin_test",
        email="admin@test.com",
        password="TestPassword123!",
    )


@pytest.fixture
def departamento(db):
    return Departamento.objects.create(nombre="Tecnología", descripcion="Área de TI")


@pytest.fixture
def cargo(departamento):
    return Cargo.objects.create(
        nombre="Desarrollador",
        departamento=departamento,
        nivel_riesgo_arl=1,
    )


@pytest.fixture
def empleado(db):
    return Empleado.objects.create(
        tipo_documento="CC",
        numero_documento="1234567890",
        primer_nombre="Juan",
        primer_apellido="Pérez",
        fecha_nacimiento=date(1990, 5, 15),
        direccion="Calle 123 #45-67",
        telefono="3001234567",
        eps="Sura",
        fondo_pension="Porvenir",
    )


@pytest.fixture
def contrato(empleado, cargo):
    return Contrato.objects.create(
        empleado=empleado,
        cargo=cargo,
        tipo_contrato="TI",
        fecha_inicio=date(2024, 1, 1),
        salario_base=Decimal("1300000"),
        auxilio_transporte=True,
    )


@pytest.fixture
def parametros_2026(db):
    """Parámetros de nómina para el año 2026 (valores estimados)."""
    return ParametroNomina.objects.create(
        anio=2026,
        smmlv=Decimal("1423500"),
        auxilio_transporte=Decimal("200000"),
        porcentaje_salud_empleado=Decimal("4.00"),
        porcentaje_salud_empleador=Decimal("8.50"),
        porcentaje_pension_empleado=Decimal("4.00"),
        porcentaje_pension_empleador=Decimal("12.00"),
        porcentaje_arl_base=Decimal("0.5220"),
        porcentaje_sena=Decimal("2.00"),
        porcentaje_icbf=Decimal("3.00"),
        porcentaje_caja_compensacion=Decimal("4.00"),
    )


@pytest.fixture
def periodo(parametros_2026, admin_user):
    return PeriodoNomina.objects.create(
        nombre="Septiembre 2026",
        fecha_inicio=date(2026, 9, 1),
        fecha_fin=date(2026, 9, 30),
        parametros=parametros_2026,
        creado_por=admin_user,
    )
