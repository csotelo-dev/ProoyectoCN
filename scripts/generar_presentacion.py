"""Genera la presentacion PDF del proyecto SIRH Nomina."""

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

W, H = landscape(A4)

# Colores HR
PRIMARY = colors.HexColor("#1e6b8a")
ACCENT = colors.HexColor("#2a9d8f")
DARK = colors.HexColor("#1a2332")
TEXT = colors.HexColor("#3d4f5f")
MUTED = colors.HexColor("#7a8a9e")
LIGHT_BG = colors.HexColor("#f5f6f8")
WHITE = colors.white
SUCCESS = colors.HexColor("#2d6a4f")
DANGER = colors.HexColor("#c0392b")
WARNING = colors.HexColor("#b8860b")

# Estilos
s_title = ParagraphStyle("title", fontSize=28, fontName="Helvetica-Bold", textColor=PRIMARY, leading=34, alignment=TA_LEFT)
s_subtitle = ParagraphStyle("subtitle", fontSize=14, fontName="Helvetica", textColor=MUTED, leading=20)
s_slide_title = ParagraphStyle("slide_title", fontSize=22, fontName="Helvetica-Bold", textColor=PRIMARY, leading=28, spaceBefore=0, spaceAfter=12)
s_h3 = ParagraphStyle("h3", fontSize=13, fontName="Helvetica-Bold", textColor=DARK, leading=18, spaceBefore=10, spaceAfter=4)
s_body = ParagraphStyle("body", fontSize=11, fontName="Helvetica", textColor=TEXT, leading=16, spaceBefore=2, spaceAfter=2)
s_bullet = ParagraphStyle("bullet", fontSize=11, fontName="Helvetica", textColor=TEXT, leading=16, leftIndent=16, bulletIndent=4, spaceBefore=2, spaceAfter=2)
s_small = ParagraphStyle("small", fontSize=9, fontName="Helvetica", textColor=MUTED, leading=12)
s_cover_title = ParagraphStyle("cover_title", fontSize=34, fontName="Helvetica-Bold", textColor=PRIMARY, leading=42, alignment=TA_CENTER)
s_cover_sub = ParagraphStyle("cover_sub", fontSize=14, fontName="Helvetica", textColor=TEXT, leading=20, alignment=TA_CENTER)
s_cover_meta = ParagraphStyle("cover_meta", fontSize=11, fontName="Helvetica", textColor=MUTED, leading=16, alignment=TA_CENTER)
s_big_number = ParagraphStyle("big_number", fontSize=36, fontName="Helvetica-Bold", textColor=ACCENT, leading=40, alignment=TA_CENTER)
s_center = ParagraphStyle("center", fontSize=11, fontName="Helvetica", textColor=TEXT, leading=16, alignment=TA_CENTER)
s_mono = ParagraphStyle("mono", fontSize=9, fontName="Courier", textColor=DARK, leading=13, spaceBefore=4, spaceAfter=4)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(2*cm, 1*cm, "SIRH Nomina — Cesar Augusto Sotelo Zapata — UCN — Computacion en la Nube — Septiembre 2026")
    canvas.drawRightString(W - 2*cm, 1*cm, f"{doc.page}")
    canvas.restoreState()

def make_table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXT),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e7ed")),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
        ]
    t.setStyle(TableStyle(style))
    return t

output = "D:/UCN/SEMESTRE 9/COMPUTACIÓN EN LA NUBE/PROYECTOUCN/docs/presentacion.pdf"
doc = SimpleDocTemplate(output, pagesize=landscape(A4), leftMargin=2.5*cm, rightMargin=2.5*cm, topMargin=2*cm, bottomMargin=2*cm)
story = []

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 1: PORTADA
# ═══════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 4*cm))
story.append(Paragraph("SIRH Nomina", s_cover_title))
story.append(Spacer(1, 6*mm))
story.append(Paragraph("Sistema de Gestion de Talento Humano<br/>y Liquidacion de Nomina en Pymes", s_cover_sub))
story.append(Spacer(1, 2*cm))
story.append(Paragraph("Curso: Computacion en la Nube — UCN<br/>Autor: Cesar Augusto Sotelo Zapata<br/>Metodologia: DevOps / CI-CD<br/>Infraestructura: Linode (Akamai Cloud) — IaaS — USD $7/mes<br/>Repositorio: github.com/csotelo-dev/ProoyectoCN", s_cover_meta))
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("Taller ABP — Entrega 1: Ecosistema Interactivo Cloud — Septiembre 2026", s_small))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 2: PROBLEMA
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("1. Planteamiento del Problema", s_slide_title))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("<b>Situacion actual en Pymes colombianas</b>", s_h3))
story.append(Paragraph("Las pymes gestionan los procesos de talento humano (contratacion, novedades, vacaciones, liquidacion de nomina) de forma manual o con hojas de calculo dispersas.", s_body))
story.append(Spacer(1, 3*mm))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Errores de liquidacion</b> con impacto economico directo en los pagos a empleados", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Sin trazabilidad</b> ni control de versiones en los datos de nomina", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Reprocesos administrativos</b> y demoras en atencion de solicitudes", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Riesgo normativo:</b> incumplimiento de la Ley 1581/2012 (datos personales)", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Sin canal de autoconsulta</b> para los empleados", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Costo fijo on-premise:</b> ~USD $120/mes (hardware, energia, licencias, soporte)", s_bullet))
story.append(Spacer(1, 6*mm))
story.append(Paragraph("<b>Pregunta Problema</b>", s_h3))
story.append(Paragraph("<i>¿De que manera un sistema de gestion de talento humano y nomina desplegado en un VPS (IaaS) de Linode permite reducir los errores de liquidacion, automatizar los procesos administrativos y disminuir en mas de un 90% el costo fijo mensual de infraestructura?</i>", s_body))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 3: SOLUCION
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("2. Solucion Propuesta", s_slide_title))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Sistema web que automatiza la gestion de talento humano y liquidacion de nomina colombiana, desplegado en la nube con un ahorro del 94.2% en costos de infraestructura.", s_body))
story.append(Spacer(1, 6*mm))

data = [["Metrica", "Valor", "Como se logra"],
    ["Reduccion de errores", "90%", "Motor de liquidacion automatizado con exactitud >= 99%"],
    ["Tiempo de atencion", "-60%", "Portal de autoconsulta via API REST para empleados"],
    ["Ahorro infraestructura", "94.2%", "Migracion de on-premise ($120) a Linode IaaS ($7/mes)"]]
story.append(make_table(data, col_widths=[5*cm, 3*cm, 14*cm]))
story.append(Spacer(1, 8*mm))

story.append(Paragraph("<b>Modulos del Sistema</b>", s_h3))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Core (Talento Humano):</b> CRUD de empleados, departamentos, cargos, contratos. Control de acceso por roles (administrador, gestion humana, empleado).", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Payroll (Nomina):</b> Motor de liquidacion colombiana — parametros legales, novedades, horas extra, seguridad social, parafiscales. Desprendibles de pago.", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>API REST (Autoconsulta):</b> Endpoints para que empleados consulten sus desprendibles, contratos y datos personales.", s_bullet))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 4: ARQUITECTURA
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("3. Arquitectura Cloud (IaaS — Linode)", s_slide_title))
story.append(Spacer(1, 4*mm))
arch = """
   Linode Nanode 1GB  |  Ubuntu 24.04 LTS  |  Docker Compose
   ┌─────────────────────────────────────────────────────────┐
   │                                                         │
   │   Nginx  (reverse proxy + TLS Let's Encrypt + static)  │
   │                        │                                │
   │   Gunicorn + Django 5 (Python 3.12)                     │
   │   ┌────────┐  ┌──────────┐  ┌───────────────┐          │
   │   │  Core  │  │ Payroll  │  │   API REST    │          │
   │   │ (RRHH) │  │ (Nomina) │  │(Autoconsulta) │          │
   │   └────────┘  └──────────┘  └───────────────┘          │
   │                        │                                │
   │   PostgreSQL 16 (ACID + pgcrypto AES-256)               │
   │   Volumen persistente Docker                            │
   │                                                         │
   │   Seguridad: UFW + fail2ban + Linode Cloud Firewall     │
   └─────────────────────────────────────────────────────────┘
"""
story.append(Paragraph(arch.replace("\n", "<br/>"), s_mono))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("<b>Modelo de servicio:</b> IaaS (NIST SP 800-145). <b>Patron:</b> Arquitectura en tres capas (presentacion, logica de negocio, datos) con MTV de Django. <b>IaC:</b> Terraform (provider linode). <b>CI/CD:</b> GitHub Actions (lint → security → test → build → deploy).", s_body))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 5: STACK TECNOLOGICO
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("4. Stack Tecnologico", s_slide_title))
story.append(Spacer(1, 4*mm))
data = [["Capa", "Tecnologia", "Justificacion"],
    ["Lenguaje", "Python 3.12 LTS", "Ecosistema maduro para aplicaciones de gestion"],
    ["Framework", "Django 5 + DRF", "ORM, autenticacion, admin y API REST integrados"],
    ["Base de datos", "PostgreSQL 16", "Transacciones ACID; pgcrypto para cifrado AES-256"],
    ["Servidor", "Gunicorn + Nginx", "WSGI produccion + reverse proxy + TLS Let's Encrypt"],
    ["Contenedores", "Docker Compose", "Paridad entre entornos (Twelve-Factor App)"],
    ["IaC", "Terraform (linode)", "Aprovisionamiento declarativo y versionado del VPS"],
    ["CI/CD", "GitHub Actions", "Pipeline: lint, security, test, build, deploy"],
    ["Pruebas", "pytest + Locust", "Tests unitarios, integracion y carga (>= 99% exactitud)"],
    ["Seguridad", "Argon2, bandit", "Hashing OWASP, analisis estatico, auditoria"],
    ["Infraestructura", "Linode Nanode 1GB", "IaaS USD $5/mes + $2 backups = $7/mes total"]]
story.append(make_table(data, col_widths=[4*cm, 5*cm, 13*cm]))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Toda la pila es software libre sin costo de licenciamiento. Alternativas evaluadas: FastAPI (sin admin/auth integrado), MySQL (pgcrypto no nativo), Docker Compose vs instalacion directa.", s_small))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 6: CI/CD
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("5. DevOps: Pipeline CI/CD e IaC", s_slide_title))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("<b>Pipeline de Integracion y Despliegue Continuo (GitHub Actions)</b>", s_h3))

data = [["Etapa", "Herramienta", "Descripcion"],
    ["1. Lint", "Ruff", "Verifica calidad y estilo del codigo Python (PEP 8)"],
    ["2. Security", "Bandit", "Analisis estatico de seguridad del codigo fuente"],
    ["3. Test", "pytest + PostgreSQL", "20 tests automatizados con BD real (no mocks)"],
    ["4. Build", "Docker", "Construccion de imagen multi-stage para produccion"],
    ["5. Deploy", "SSH → Linode", "Despliegue automatico al VPS via llaves SSH"]]
story.append(make_table(data, col_widths=[3*cm, 5*cm, 14*cm]))
story.append(Spacer(1, 8*mm))

story.append(Paragraph("<b>Infraestructura como Codigo (Terraform)</b>", s_h3))
story.append(Paragraph("<bullet>&bull;</bullet> <b>main.tf:</b> Aprovisiona VPS Nanode 1GB + Linode Cloud Firewall (puertos 80, 443, 22 restringido)", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>cloud-init.yaml:</b> Instala Docker, configura swap 2GB, SSH hardening (ed25519), fail2ban, UFW, unattended-upgrades", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>variables.tf:</b> Token Linode (sensitive), region, llave SSH, IPs administrativas", s_bullet))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Basado en: The DevOps Handbook (Kim et al., 2021), Continuous Integration (Fowler, 2006), Infrastructure as Code (Morris, 2020).", s_small))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 7: SEGURIDAD
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("6. Seguridad y Cumplimiento Normativo", s_slide_title))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("<b>Defensa en profundidad</b>", s_h3))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Red:</b> Linode Cloud Firewall + UFW + fail2ban. SSH solo con llaves ed25519, root login deshabilitado.", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Cifrado en transito:</b> TLS 1.2+ con certificados Let's Encrypt (renovacion automatica).", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Cifrado en reposo:</b> pgcrypto/AES-256 para campos sensibles de nomina.", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Autenticacion:</b> Contraseñas con Argon2 (OWASP). Validacion minima 10 caracteres.", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Autorizacion:</b> Control de acceso por roles con principio de minimo privilegio.", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Auditoria:</b> Middleware que registra todas las operaciones de escritura.", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Hardening:</b> CIS Benchmark Ubuntu, parches automaticos (unattended-upgrades).", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> <b>Headers HTTP:</b> HSTS, X-Frame-Options DENY, X-Content-Type-Options, Referrer-Policy.", s_bullet))
story.append(Spacer(1, 6*mm))

data = [["Marco Normativo", "Implementacion"],
    ["Ley 1581/2012", "Cifrado de datos personales, control de acceso, auditoria, consentimiento"],
    ["ISO/IEC 27001", "Politica de acceso, gestion de llaves, monitoreo continuo"],
    ["NIST CSF 2.0", "Identificar, Proteger, Detectar (fail2ban), Responder, Recuperar (backups)"],
    ["CIS Benchmark", "Hardening Ubuntu via cloud-init, actualizaciones automaticas"],
    ["OWASP Top 10", "Argon2, CSRF, XSS, SQL injection prevention (ORM Django)"]]
story.append(make_table(data, col_widths=[5*cm, 17*cm]))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 8: PRESUPUESTO
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("7. Presupuesto Cloud", s_slide_title))
story.append(Spacer(1, 4*mm))

data = [["Servicio", "Proveedor", "Detalle", "USD/mes"],
    ["Nanode 1GB", "Linode (Akamai)", "1 vCPU, 1GB RAM, 25GB SSD, 1TB transfer", "$5.00"],
    ["Backups automaticos", "Linode (Akamai)", "Copias diarias y semanales", "$2.00"],
    ["TOTAL", "", "", "$7.00"]]
story.append(make_table(data, col_widths=[5*cm, 5*cm, 9*cm, 3*cm]))
story.append(Spacer(1, 8*mm))

data2 = [["Concepto", "On-Premise", "Linode Cloud", "Ahorro"],
    ["Costo mensual", "$120 USD", "$7 USD", "94.2%"],
    ["Costo anual", "$1,440 USD", "$84 USD", "$1,356 USD"]]
story.append(make_table(data2, col_widths=[6*cm, 5*cm, 5*cm, 6*cm]))
story.append(Spacer(1, 6*mm))

story.append(Paragraph("<b>Ruta de escalamiento:</b> Si 1GB de RAM resulta insuficiente, migrar a Linode 2GB ($12/mes, 2 vCPU, 50GB SSD) mediante resize sin reinstalacion.", s_body))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Fuente: Akamai Cloud Computing Pricing — North America (septiembre 2026).", s_small))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 9: RESULTADOS
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("8. Resultados y Pruebas", s_slide_title))
story.append(Spacer(1, 4*mm))

story.append(Paragraph("<b>Suite de pruebas automatizadas (pytest)</b>", s_h3))
data = [["Modulo", "Tests", "Cobertura"],
    ["Core (modelos, vistas, auth)", "7 tests", "CRUD, autenticacion, permisos"],
    ["Payroll (liquidacion nomina)", "9 tests", "Motor de nomina completo"],
    ["API REST (endpoints)", "4 tests", "Permisos, autoconsulta"],
    ["TOTAL", "20 tests", "Exactitud >= 99%"]]
story.append(make_table(data, col_widths=[7*cm, 4*cm, 11*cm]))
story.append(Spacer(1, 6*mm))

story.append(Paragraph("<b>Validaciones del motor de nomina colombiana</b>", s_h3))
story.append(Paragraph("<bullet>&bull;</bullet> Salario proporcional, auxilio de transporte (si salario <= 2 SMMLV)", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> Horas extra con factores legales (diurna 25%, nocturna 75%, dominical 100%, 150%)", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> Aportes seguridad social: salud 4%, pension 4% (empleado); 8.5%, 12% (empleador)", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> Parafiscales: SENA 2%, ICBF 3%, Caja de Compensacion 4%", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> Bonificaciones, deducciones, re-liquidacion sin duplicados", s_bullet))
story.append(Spacer(1, 6*mm))

story.append(Paragraph("<b>Estructura del repositorio:</b> 72 archivos organizados por capas. README.md profesional con diagramas de arquitectura, instrucciones de despliegue y referencias.", s_body))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 10: CONCLUSIONES Y REFERENCIAS
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("9. Conclusiones y Referencias", s_slide_title))
story.append(Spacer(1, 4*mm))

story.append(Paragraph("<b>Conclusiones</b>", s_h3))
story.append(Paragraph("<bullet>&bull;</bullet> La migracion a IaaS (Linode) reduce el costo de infraestructura en un <b>94.2%</b> ($120 → $7 USD/mes).", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> El motor de liquidacion automatizada elimina errores humanos con exactitud <b>>= 99%</b>.", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> La API REST de autoconsulta reduce la carga administrativa en <b>60%</b>.", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> La estrategia DevOps/CI-CD garantiza <b>entregas repetibles y trazables</b>.", s_bullet))
story.append(Paragraph("<bullet>&bull;</bullet> El cumplimiento de Ley 1581/2012, ISO 27001 y NIST CSF 2.0 mitiga el riesgo normativo.", s_bullet))
story.append(Spacer(1, 8*mm))

story.append(Paragraph("<b>Referencias</b>", s_h3))
refs = [
    "Mell, P. y Grance, T. (2011). The NIST Definition of Cloud Computing. NIST SP 800-145.",
    "Kim, G., Humble, J., Debois, P. y Willis, J. (2021). The DevOps Handbook (2a ed.).",
    "Morris, K. (2020). Infrastructure as Code (2a ed.). O'Reilly Media.",
    "Fowler, M. (2006). Continuous Integration. martinfowler.com.",
    "Wiggins, A. (2017). The Twelve-Factor App. 12factor.net.",
    "Pressman, R. S. y Maxim, B. R. (2021). Ingenieria del software (9a ed.). McGraw-Hill.",
    "ISO/IEC 25010:2011 — Modelos de calidad. ISO/IEC 27001:2022 — SGSI.",
    "NIST (2024). Cybersecurity Framework (CSF) 2.0.",
    "OWASP Foundation (2021). OWASP Top 10.",
    "Ley 1581/2012 y Decreto 1377/2013 — Proteccion de datos personales (Colombia).",
    "Akamai Technologies (2026). Cloud Computing Pricing — North America.",
]
for r in refs:
    story.append(Paragraph(f"<bullet>&bull;</bullet> {r}", ParagraphStyle("ref", parent=s_bullet, fontSize=9, leading=13)))

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"PDF generado: {output}")
