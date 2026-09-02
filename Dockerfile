# =============================================================================
# Dockerfile — Sistema de Gestión de Talento Humano y Nómina
# Multi-stage build para imagen mínima de producción
# =============================================================================

# --- Stage 1: Builder --------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Stage 2: Production ----------------------------------------------------
FROM python:3.12-slim

# Evitar crear archivos .pyc y forzar stdout sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Crear usuario no-root (principio de mínimo privilegio)
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copiar dependencias instaladas
COPY --from=builder /install /usr/local

# Copiar código fuente
COPY nomina/ .

# Recolectar archivos estáticos
RUN DJANGO_SECRET_KEY=build-placeholder python manage.py collectstatic --noinput 2>/dev/null || true

# Cambiar a usuario no-root
USER appuser

EXPOSE 8000

# Gunicorn con configuración optimizada para Nanode 1GB
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--threads", "2", \
     "--worker-class", "gthread", \
     "--worker-tmp-dir", "/dev/shm", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
