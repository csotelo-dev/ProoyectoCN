"""Tests del módulo Core — Modelos y Vistas."""

from datetime import date
from decimal import Decimal

import pytest
from django.db import IntegrityError
from django.test import Client
from django.urls import reverse

from core.models import Departamento, Empleado


@pytest.mark.django_db
class TestDepartamento:
    def test_crear_departamento(self, departamento):
        assert departamento.nombre == "Tecnología"
        assert departamento.activo is True
        assert str(departamento) == "Tecnología"

    def test_departamento_unico(self, departamento):
        with pytest.raises(IntegrityError):
            Departamento.objects.create(nombre="Tecnología")


@pytest.mark.django_db
class TestCargo:
    def test_crear_cargo(self, cargo):
        assert cargo.nombre == "Desarrollador"
        assert cargo.nivel_riesgo_arl == 1

    def test_str_cargo(self, cargo):
        assert "Desarrollador" in str(cargo)
        assert "Tecnología" in str(cargo)


@pytest.mark.django_db
class TestEmpleado:
    def test_crear_empleado(self, empleado):
        assert empleado.numero_documento == "1234567890"
        assert empleado.activo is True

    def test_nombre_completo(self, empleado):
        assert empleado.nombre_completo == "Juan Pérez"

    def test_documento_unico(self, empleado):
        with pytest.raises(IntegrityError):
            Empleado.objects.create(
                numero_documento="1234567890",
                primer_nombre="Otro",
                primer_apellido="Empleado",
                fecha_nacimiento=date(1995, 1, 1),
                direccion="Otra dirección",
                telefono="3009999999",
                eps="Nueva EPS",
                fondo_pension="Protección",
            )


@pytest.mark.django_db
class TestContrato:
    def test_crear_contrato(self, contrato):
        assert contrato.salario_base == Decimal("1300000")
        assert contrato.tipo_contrato == "TI"

    def test_contrato_vigente(self, contrato):
        assert contrato.vigente is True

    def test_contrato_terminado(self, contrato):
        contrato.fecha_fin = date(2024, 1, 1)
        contrato.save()
        assert contrato.vigente is False


@pytest.mark.django_db
class TestVistasDashboard:
    def test_dashboard_requiere_login(self):
        client = Client()
        response = client.get(reverse("dashboard"))
        assert response.status_code == 302  # Redirect to login

    def test_dashboard_autenticado(self, admin_user):
        client = Client()
        client.force_login(admin_user)
        response = client.get(reverse("dashboard"))
        assert response.status_code == 200

    def test_login_page(self):
        client = Client()
        response = client.get(reverse("login"))
        assert response.status_code == 200
