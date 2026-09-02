"""Serializers — API REST para autoconsulta de empleados."""

from core.models import Cargo, Contrato, Departamento, Empleado
from payroll.models import Nomina, PeriodoNomina
from rest_framework import serializers


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ["id", "nombre", "descripcion", "activo"]


class CargoSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source="departamento.nombre", read_only=True)

    class Meta:
        model = Cargo
        fields = ["id", "nombre", "departamento", "departamento_nombre", "nivel_riesgo_arl"]


class EmpleadoSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.CharField(read_only=True)

    class Meta:
        model = Empleado
        fields = [
            "id",
            "tipo_documento",
            "numero_documento",
            "nombre_completo",
            "primer_nombre",
            "primer_apellido",
            "eps",
            "fondo_pension",
            "activo",
        ]


class ContratoSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source="empleado.nombre_completo", read_only=True)
    cargo_nombre = serializers.CharField(source="cargo.nombre", read_only=True)

    class Meta:
        model = Contrato
        fields = [
            "id",
            "empleado",
            "empleado_nombre",
            "cargo",
            "cargo_nombre",
            "tipo_contrato",
            "fecha_inicio",
            "fecha_fin",
            "salario_base",
            "activo",
        ]


class NominaSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(
        source="contrato.empleado.nombre_completo", read_only=True
    )
    periodo_nombre = serializers.CharField(source="periodo.nombre", read_only=True)

    class Meta:
        model = Nomina
        fields = [
            "id",
            "periodo",
            "periodo_nombre",
            "empleado_nombre",
            "dias_trabajados",
            "salario_base",
            "auxilio_transporte",
            "total_horas_extra",
            "total_bonificaciones",
            "total_devengado",
            "aporte_salud_empleado",
            "aporte_pension_empleado",
            "total_otras_deducciones",
            "total_deducciones",
            "neto_pagar",
            "liquidado_en",
        ]
        read_only_fields = fields


class PeriodoNominaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoNomina
        fields = ["id", "nombre", "fecha_inicio", "fecha_fin", "estado"]
