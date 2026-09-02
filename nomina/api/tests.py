"""Tests de la API REST — Autoconsulta de empleados."""

import pytest
from django.test import Client


@pytest.mark.django_db
class TestAPIEndpoints:
    def test_api_requiere_autenticacion(self):
        client = Client()
        response = client.get("/api/departamentos/")
        assert response.status_code == 403

    def test_api_departamentos_autenticado(self, admin_user, departamento):
        client = Client()
        client.force_login(admin_user)
        response = client.get("/api/departamentos/")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1

    def test_api_empleados_staff_ve_todos(self, admin_user, empleado):
        client = Client()
        client.force_login(admin_user)
        response = client.get("/api/empleados/")
        assert response.status_code == 200

    def test_api_mi_ultimo_desprendible_sin_nomina(self, admin_user):
        client = Client()
        client.force_login(admin_user)
        response = client.get("/api/nominas/mi_ultimo_desprendible/")
        assert response.status_code == 404
