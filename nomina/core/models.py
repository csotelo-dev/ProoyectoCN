"""
Modelos del módulo Core — Gestión de Talento Humano.

Entidades: Departamento, Cargo, Empleado, Contrato, RegistroAuditoria.
Seguridad: los campos sensibles (salario, documento) se marcan para
cifrado en reposo con pgcrypto en la capa de base de datos.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone


class Departamento(models.Model):
    """Unidad organizacional de la empresa."""

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "departamentos"

    def __str__(self):
        return self.nombre


class Cargo(models.Model):
    """Cargo o puesto de trabajo dentro de un departamento."""

    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(
        Departamento, on_delete=models.PROTECT, related_name="cargos"
    )
    nivel_riesgo_arl = models.PositiveSmallIntegerField(
        default=1,
        help_text="Nivel de riesgo ARL (1-5)",
    )
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["departamento", "nombre"]
        unique_together = ["nombre", "departamento"]

    def __str__(self):
        return f"{self.nombre} — {self.departamento}"


class Empleado(models.Model):
    """Persona vinculada a la empresa."""

    TIPO_DOCUMENTO_CHOICES = [
        ("CC", "Cédula de Ciudadanía"),
        ("CE", "Cédula de Extranjería"),
        ("PA", "Pasaporte"),
        ("TI", "Tarjeta de Identidad"),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="empleado",
        null=True,
        blank=True,
    )
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES, default="CC")
    numero_documento = models.CharField(max_length=20, unique=True)
    primer_nombre = models.CharField(max_length=60)
    segundo_nombre = models.CharField(max_length=60, blank=True)
    primer_apellido = models.CharField(max_length=60)
    segundo_apellido = models.CharField(max_length=60, blank=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email_personal = models.EmailField(blank=True)
    eps = models.CharField("EPS", max_length=100)
    fondo_pension = models.CharField(max_length=100)
    fondo_cesantias = models.CharField(max_length=100, blank=True)
    caja_compensacion = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)
    foto = models.ImageField(upload_to="empleados/fotos/", blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["primer_apellido", "primer_nombre"]

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} ({self.numero_documento})"

    @property
    def nombre_completo(self):
        partes = [self.primer_nombre, self.segundo_nombre, self.primer_apellido, self.segundo_apellido]
        return " ".join(p for p in partes if p)


class Contrato(models.Model):
    """Contrato laboral que vincula un empleado con un cargo."""

    TIPO_CONTRATO_CHOICES = [
        ("TI", "Término Indefinido"),
        ("TF", "Término Fijo"),
        ("OL", "Obra o Labor"),
        ("AP", "Aprendizaje"),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name="contratos")
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, related_name="contratos")
    tipo_contrato = models.CharField(max_length=2, choices=TIPO_CONTRATO_CHOICES, default="TI")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    salario_base = models.DecimalField(max_digits=12, decimal_places=2)
    auxilio_transporte = models.BooleanField(
        default=True,
        help_text="Aplica si el salario es <= 2 SMMLV",
    )
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"{self.empleado} — {self.cargo} ({self.get_tipo_contrato_display()})"

    @property
    def vigente(self):
        hoy = timezone.now().date()
        if self.fecha_fin:
            return self.fecha_inicio <= hoy <= self.fecha_fin and self.activo
        return self.fecha_inicio <= hoy and self.activo


class RegistroAuditoria(models.Model):
    """Log de auditoría para trazabilidad de operaciones sensibles."""

    ACCION_CHOICES = [
        ("CREATE", "Creación"),
        ("UPDATE", "Actualización"),
        ("DELETE", "Eliminación"),
        ("LOGIN", "Inicio de Sesión"),
        ("LOGOUT", "Cierre de Sesión"),
        ("LIQUIDAR", "Liquidación de Nómina"),
        ("VIEW", "Consulta"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="registros_auditoria",
    )
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES)
    modelo = models.CharField(max_length=100)
    objeto_id = models.CharField(max_length=50, blank=True)
    detalle = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "registro de auditoría"
        verbose_name_plural = "registros de auditoría"

    def __str__(self):
        return f"{self.timestamp:%Y-%m-%d %H:%M} | {self.usuario} | {self.accion} | {self.modelo}"
