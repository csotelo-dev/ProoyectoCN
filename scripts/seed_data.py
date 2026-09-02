#!/usr/bin/env python
"""
Script de datos semilla — Crea datos iniciales para demostración.

Uso: docker compose exec web python manage.py shell < ../scripts/seed_data.py
  O: cd nomina && python manage.py shell < ../scripts/seed_data.py
"""

import os
import sys
from datetime import date
from decimal import Decimal

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "nomina"))
django.setup()

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

from core.models import Cargo, Contrato, Departamento, Empleado
from payroll.models import Novedad, ParametroNomina, PeriodoNomina
from payroll.services import liquidar_periodo_completo

print("=== Creando datos semilla ===")

# --- Grupos y permisos -------------------------------------------------------
grupo_admin, _ = Group.objects.get_or_create(name="administrador")
grupo_rrhh, _ = Group.objects.get_or_create(name="gestion_humana")
grupo_empleado, _ = Group.objects.get_or_create(name="empleado")

# Asignar todos los permisos al grupo administrador
for perm in Permission.objects.all():
    grupo_admin.permissions.add(perm)

# RRHH: permisos de core y payroll
for app_label in ["core", "payroll"]:
    for perm in Permission.objects.filter(content_type__app_label=app_label):
        grupo_rrhh.permissions.add(perm)

# Empleado: solo lectura
for perm in Permission.objects.filter(codename__startswith="view_"):
    grupo_empleado.permissions.add(perm)

print("  Grupos creados: administrador, gestion_humana, empleado")

# --- Superusuario ------------------------------------------------------------
if not User.objects.filter(username="admin").exists():
    admin_user = User.objects.create_superuser("admin", "admin@sirh.com", "Admin2026!")
    admin_user.groups.add(grupo_admin)
    print("  Superusuario creado: admin / Admin2026!")

# --- Parámetros de nómina 2026 -----------------------------------------------
params, created = ParametroNomina.objects.get_or_create(
    anio=2026,
    defaults={
        "smmlv": Decimal("1423500"),
        "auxilio_transporte": Decimal("200000"),
    },
)
if created:
    print(f"  Parámetros 2026: SMMLV=${params.smmlv:,.0f}")

# --- Departamentos -----------------------------------------------------------
departamentos_data = [
    ("Administración", "Dirección general y administrativa"),
    ("Tecnología", "Desarrollo de software y soporte TI"),
    ("Gestión Humana", "Recursos humanos y bienestar"),
    ("Comercial", "Ventas y servicio al cliente"),
    ("Contabilidad", "Área contable y financiera"),
]
departamentos = {}
for nombre, desc in departamentos_data:
    dep, _ = Departamento.objects.get_or_create(nombre=nombre, defaults={"descripcion": desc})
    departamentos[nombre] = dep
print(f"  {len(departamentos)} departamentos creados")

# --- Cargos ------------------------------------------------------------------
cargos_data = [
    ("Gerente General", "Administración", 1),
    ("Desarrollador Senior", "Tecnología", 1),
    ("Desarrollador Junior", "Tecnología", 1),
    ("Coordinador RRHH", "Gestión Humana", 1),
    ("Analista de Nómina", "Gestión Humana", 1),
    ("Ejecutivo Comercial", "Comercial", 2),
    ("Contador", "Contabilidad", 1),
    ("Auxiliar Contable", "Contabilidad", 1),
]
cargos = {}
for nombre, dep_nombre, riesgo in cargos_data:
    cargo, _ = Cargo.objects.get_or_create(
        nombre=nombre,
        departamento=departamentos[dep_nombre],
        defaults={"nivel_riesgo_arl": riesgo},
    )
    cargos[nombre] = cargo
print(f"  {len(cargos)} cargos creados")

# --- Empleados y Contratos ---------------------------------------------------
empleados_data = [
    {
        "doc": "1098765432", "nombre": "María", "apellido": "García",
        "nacimiento": date(1985, 3, 12), "eps": "Sura", "pension": "Porvenir",
        "cargo": "Gerente General", "salario": Decimal("6500000"), "auxilio": False,
    },
    {
        "doc": "1087654321", "nombre": "Carlos", "apellido": "Rodríguez",
        "nacimiento": date(1990, 7, 22), "eps": "Nueva EPS", "pension": "Protección",
        "cargo": "Desarrollador Senior", "salario": Decimal("4200000"), "auxilio": False,
    },
    {
        "doc": "1076543210", "nombre": "Ana", "apellido": "Martínez",
        "nacimiento": date(1995, 11, 5), "eps": "Sanitas", "pension": "Porvenir",
        "cargo": "Desarrollador Junior", "salario": Decimal("1800000"), "auxilio": True,
    },
    {
        "doc": "1065432109", "nombre": "Luis", "apellido": "López",
        "nacimiento": date(1988, 1, 30), "eps": "Compensar", "pension": "Colfondos",
        "cargo": "Coordinador RRHH", "salario": Decimal("3200000"), "auxilio": False,
    },
    {
        "doc": "1054321098", "nombre": "Sofía", "apellido": "Hernández",
        "nacimiento": date(1992, 9, 18), "eps": "Sura", "pension": "Protección",
        "cargo": "Analista de Nómina", "salario": Decimal("2400000"), "auxilio": True,
    },
    {
        "doc": "1043210987", "nombre": "Andrés", "apellido": "Torres",
        "nacimiento": date(1993, 4, 8), "eps": "Nueva EPS", "pension": "Porvenir",
        "cargo": "Ejecutivo Comercial", "salario": Decimal("1500000"), "auxilio": True,
    },
    {
        "doc": "1032109876", "nombre": "Laura", "apellido": "Ramírez",
        "nacimiento": date(1987, 12, 25), "eps": "Sanitas", "pension": "Colfondos",
        "cargo": "Contador", "salario": Decimal("3800000"), "auxilio": False,
    },
    {
        "doc": "1021098765", "nombre": "Diego", "apellido": "Vargas",
        "nacimiento": date(1996, 6, 14), "eps": "Compensar", "pension": "Protección",
        "cargo": "Auxiliar Contable", "salario": Decimal("1423500"), "auxilio": True,
    },
]

for data in empleados_data:
    emp, created = Empleado.objects.get_or_create(
        numero_documento=data["doc"],
        defaults={
            "primer_nombre": data["nombre"],
            "primer_apellido": data["apellido"],
            "fecha_nacimiento": data["nacimiento"],
            "direccion": "Calle 100 #10-20, Bogotá",
            "telefono": "300" + data["doc"][-7:],
            "eps": data["eps"],
            "fondo_pension": data["pension"],
            "fondo_cesantias": data["pension"],
            "caja_compensacion": "Compensar",
        },
    )
    if created:
        Contrato.objects.create(
            empleado=emp,
            cargo=cargos[data["cargo"]],
            tipo_contrato="TI",
            fecha_inicio=date(2024, 1, 15),
            salario_base=data["salario"],
            auxilio_transporte=data["auxilio"],
        )

print(f"  {len(empleados_data)} empleados con contratos creados")

# --- Periodo de nómina y novedades de ejemplo --------------------------------
periodo, created = PeriodoNomina.objects.get_or_create(
    nombre="Septiembre 2026",
    defaults={
        "fecha_inicio": date(2026, 9, 1),
        "fecha_fin": date(2026, 9, 30),
        "parametros": params,
        "creado_por": User.objects.get(username="admin"),
    },
)

if created:
    # Novedades de ejemplo
    andres = Empleado.objects.get(numero_documento="1043210987")
    Novedad.objects.create(
        periodo=periodo, empleado=andres,
        tipo="COMISION", valor=Decimal("350000"),
        observacion="Comisión ventas septiembre",
    )

    carlos = Empleado.objects.get(numero_documento="1087654321")
    Novedad.objects.create(
        periodo=periodo, empleado=carlos,
        tipo="HE_DIURNA", cantidad=Decimal("8"),
        observacion="Soporte deploy en producción",
    )

    diego = Empleado.objects.get(numero_documento="1021098765")
    Novedad.objects.create(
        periodo=periodo, empleado=diego,
        tipo="BONIFICACION", valor=Decimal("100000"),
        observacion="Bonificación por cumplimiento",
    )

    print("  Periodo Septiembre 2026 creado con novedades de ejemplo")

    # Liquidar el periodo
    admin = User.objects.get(username="admin")
    nominas = liquidar_periodo_completo(periodo, admin)
    print(f"  Periodo liquidado: {len(nominas)} nóminas procesadas")

print("\n=== Datos semilla completados ===")
print("Acceder al sistema: http://localhost:8000")
print("Usuario: admin | Contraseña: Admin2026!")
