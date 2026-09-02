# SIRH Nomina — Sistema de Gestion de Talento Humano y Liquidacion de Nomina

**Sistema de informacion para la gestion del talento humano y liquidacion de nomina en pymes**, desplegado en infraestructura IaaS de Linode (Akamai Cloud).

| | |
|---|---|
| **Curso** | Computacion en la Nube — UCN |
| **Autor** | Cesar Augusto Sotelo Zapata |
| **Metodologia** | DevOps / CI-CD |
| **Infraestructura** | Linode Nanode 1GB (IaaS) — USD $7/mes |
| **Entrega** | Taller ABP — Entrega 1: Ecosistema Interactivo Cloud |

---

## Problema

Las pymes gestionan los procesos de talento humano (contratacion, novedades, vacaciones, liquidacion de nomina) de forma manual o con hojas de calculo dispersas, generando:

- Errores en el calculo de la nomina con impacto economico directo
- Falta de trazabilidad y control de versiones
- Riesgo de incumplimiento normativo (Ley 1581 de 2012 — datos personales)
- Costo fijo de infraestructura on-premise de ~USD $120/mes

## Solucion

Sistema web que automatiza la gestion de talento humano y liquidacion de nomina colombiana, desplegado en la nube con un ahorro del **94.2%** en costos de infraestructura.

---

## Arquitectura

```
                        ┌─────────────────────────────────────────┐
                        │        Linode Nanode 1GB (IaaS)         │
                        │        Ubuntu 24.04 LTS + Docker        │
                        │  ┌─────────────────────────────────┐    │
    Internet ──────────►│  │         Nginx (puerto 80/443)    │    │
        HTTPS           │  │   Reverse Proxy + TLS (Let's     │    │
                        │  │   Encrypt) + Archivos Estaticos  │    │
                        │  └──────────────┬──────────────────┘    │
                        │                 │                        │
                        │  ┌──────────────▼──────────────────┐    │
                        │  │    Gunicorn + Django 5 (LTS)     │    │
                        │  │  ┌───────┐ ┌────────┐ ┌─────┐   │    │
                        │  │  │ Core  │ │Payroll │ │ API │   │    │
                        │  │  │(RRHH) │ │(Nomina)│ │(REST│   │    │
                        │  │  └───────┘ └────────┘ └─────┘   │    │
                        │  └──────────────┬──────────────────┘    │
                        │                 │                        │
                        │  ┌──────────────▼──────────────────┐    │
                        │  │     PostgreSQL 16 (ACID)         │    │
                        │  │   pgcrypto (cifrado AES-256)     │    │
                        │  │   Volumen persistente Docker      │    │
                        │  └─────────────────────────────────┘    │
                        └─────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────┐
    │              GitHub Actions (CI/CD)                 │
    │  Lint (ruff) → Security (bandit) → Test (pytest)  │
    │        → Build (Docker) → Deploy (SSH)            │
    └────────────────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────┐
    │         Terraform (IaC — provider linode)          │
    │   VPS + Firewall + Cloud-Init (Hardening CIS)     │
    └────────────────────────────────────────────────────┘
```

## Stack Tecnologico

| Capa | Tecnologia | Justificacion |
|------|-----------|---------------|
| Lenguaje | Python 3.12 | Ecosistema maduro para aplicaciones de gestion |
| Framework | Django 5 + DRF | ORM, autenticacion, admin y API REST integrados |
| Base de datos | PostgreSQL 16 | Transacciones ACID, pgcrypto para cifrado |
| Servidor | Gunicorn + Nginx | WSGI produccion + reverse proxy + TLS |
| Contenedores | Docker Compose | Paridad entre entornos (Twelve-Factor App) |
| IaC | Terraform | Aprovisionamiento declarativo y versionado |
| CI/CD | GitHub Actions | Build, test, security scan y deploy automatizado |
| Seguridad | Argon2, TLS 1.2+, CIS Benchmark | Defensa en profundidad (OWASP, NIST CSF 2.0) |

## Estructura del Repositorio

```
ProoyectoCN/
├── .github/workflows/ci-cd.yml    # Pipeline CI/CD
├── nginx/                         # Configuracion Nginx (dev y prod)
├── terraform/                     # IaC — aprovisionamiento Linode
│   ├── main.tf                    # VPS + Firewall
│   ├── variables.tf
│   └── cloud-init.yaml            # Hardening CIS + Docker
├── nomina/                        # Proyecto Django
│   ├── config/                    # Settings, URLs, WSGI
│   ├── core/                      # App: Empleados, Departamentos, Contratos
│   ├── payroll/                   # App: Nomina, Liquidacion, Novedades
│   ├── api/                       # App: API REST (autoconsulta empleados)
│   ├── templates/                 # Plantillas HTML (Bootstrap 5)
│   └── static/                    # Archivos estaticos
├── scripts/seed_data.py           # Datos de prueba
├── docs/                          # Presentacion del proyecto
├── Dockerfile                     # Multi-stage build
├── docker-compose.yml             # Entorno desarrollo
├── docker-compose.prod.yml        # Entorno produccion (Linode)
├── requirements.txt               # Dependencias Python
└── .env.example                   # Variables de entorno (plantilla)
```

## Funcionalidades

### Modulo Core (Talento Humano)
- CRUD de Departamentos, Cargos, Empleados y Contratos
- Control de acceso por roles: Administrador, Gestion Humana, Empleado
- Dashboard con metricas en tiempo real
- Busqueda y paginacion

### Modulo Payroll (Nomina)
- Parametros legales de nomina por año (SMMLV, auxilio transporte, porcentajes)
- Registro de novedades: horas extra (diurnas/nocturnas/dominicales), bonificaciones, deducciones, incapacidades
- **Motor de liquidacion automatica** de nomina colombiana:
  - Salario proporcional a dias trabajados
  - Auxilio de transporte (si salario <= 2 SMMLV)
  - Horas extra con factores legales (25%, 75%, 100%, 150%)
  - Aportes a seguridad social (salud, pension, ARL)
  - Aportes parafiscales (SENA, ICBF, Caja de Compensacion)
- Desprendible de pago detallado
- Re-liquidacion sin duplicados

### API REST (Autoconsulta)
- Endpoints para consulta de empleados, contratos y desprendibles
- Endpoint `/api/nominas/mi_ultimo_desprendible/` para autoconsulta
- Control de acceso: empleados solo ven sus propios datos

### Seguridad
- Contraseñas con Argon2 (OWASP best practice)
- CSRF, XSS, Clickjacking protection (Django built-in)
- TLS 1.2+ con Let's Encrypt
- SSH solo con llaves ed25519, root login deshabilitado
- UFW + fail2ban + Linode Cloud Firewall
- Middleware de auditoria (trazabilidad de operaciones)
- Headers HTTP de seguridad (HSTS, X-Frame-Options, etc.)
- Hardening CIS Benchmark Ubuntu

## Instalacion y Despliegue

### Requisitos
- Docker y Docker Compose v2
- Git

### Desarrollo Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/csotelo-dev/ProoyectoCN.git
cd ProoyectoCN

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con valores locales

# 3. Levantar los servicios
docker compose up --build

# 4. Crear superusuario
docker compose exec web python manage.py createsuperuser

# 5. (Opcional) Cargar datos de prueba
docker compose exec web python manage.py shell < scripts/seed_data.py

# 6. Acceder al sistema
# http://localhost:8000       — Aplicacion web
# http://localhost:8000/admin — Panel de administracion
# http://localhost:8000/api/  — API REST (DRF browsable)
```

### Despliegue en Linode (Produccion)

```bash
# 1. Aprovisionar VPS con Terraform
cd terraform
terraform init
terraform plan -var="linode_token=YOUR_TOKEN" -var="ssh_public_key=YOUR_KEY"
terraform apply

# 2. Conectarse al VPS
ssh deploy@<IP_DEL_VPS>

# 3. Clonar y desplegar
cd /opt/sirh-nomina
git clone https://github.com/csotelo-dev/ProoyectoCN.git .
cp .env.example .env  # Editar con valores de produccion
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# 4. Configurar TLS (Let's Encrypt)
docker compose run --rm certbot certonly --webroot -w /var/www/certbot -d tu-dominio.com
```

### Ejecutar Tests

```bash
# Dentro del contenedor
docker compose exec web pytest --cov=. --cov-report=term-missing -v

# O localmente con virtualenv
cd nomina
pytest --cov=. -v
```

## Presupuesto Cloud

| Servicio | Proveedor | Costo Mensual (USD) |
|----------|----------|-------------------|
| Nanode 1GB (1 vCPU, 1GB RAM, 25GB SSD) | Linode (Akamai) | $5.00 |
| Backups automaticos | Linode (Akamai) | $2.00 |
| **TOTAL** | | **$7.00** |

**Ahorro vs on-premise:** $120 → $7 = **94.2% de reduccion** en costos de infraestructura.

Fuente: [Akamai Cloud Computing Pricing](https://www.akamai.com/cloud/pricing/north-america)

## Seguridad y Cumplimiento Normativo

| Requisito | Implementacion |
|-----------|---------------|
| Ley 1581 de 2012 (Datos personales) | Cifrado AES-256 (pgcrypto), control de acceso por roles, auditoria |
| ISO/IEC 27001 | SSH con llaves, MFA en Cloud Manager, principio de minimo privilegio |
| NIST CSF 2.0 | Identificar, proteger, detectar (fail2ban), responder, recuperar (backups) |
| CIS Benchmark Ubuntu | Hardening via cloud-init, parches automaticos |
| OWASP Top 10 | Argon2, CSRF, XSS protection, SQL injection prevention (ORM) |

## Referencias

- Mell, P. y Grance, T. (2011). *The NIST Definition of Cloud Computing*. NIST SP 800-145.
- Kim, G., Humble, J., Debois, P. y Willis, J. (2021). *The DevOps Handbook* (2a ed.). IT Revolution Press.
- Morris, K. (2020). *Infrastructure as Code* (2a ed.). O'Reilly Media.
- Pressman, R. S. y Maxim, B. R. (2021). *Ingenieria del software: un enfoque practico* (9a ed.). McGraw-Hill.
- Wiggins, A. (2017). *The Twelve-Factor App*. 12factor.net.
- ISO/IEC 25010:2011, ISO/IEC 27001:2022, NIST CSF 2.0.
- Congreso de Colombia. Ley 1581 de 2012 y Decreto 1377 de 2013.
- OWASP Foundation (2021). OWASP Top 10.

---

**Autor:** Cesar Augusto Sotelo Zapata — UCN, Semestre 9, Computacion en la Nube, Septiembre 2026

