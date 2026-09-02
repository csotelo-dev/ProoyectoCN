"""Formularios del módulo Core."""

from django import forms

from .models import Cargo, Contrato, Departamento, Empleado


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ["nombre", "descripcion", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ["nombre", "departamento", "nivel_riesgo_arl", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "departamento": forms.Select(attrs={"class": "form-select"}),
            "nivel_riesgo_arl": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            "tipo_documento",
            "numero_documento",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "fecha_nacimiento",
            "direccion",
            "telefono",
            "email_personal",
            "eps",
            "fondo_pension",
            "fondo_cesantias",
            "caja_compensacion",
            "activo",
        ]
        widgets = {
            "tipo_documento": forms.Select(attrs={"class": "form-select"}),
            "numero_documento": forms.TextInput(attrs={"class": "form-control"}),
            "primer_nombre": forms.TextInput(attrs={"class": "form-control"}),
            "segundo_nombre": forms.TextInput(attrs={"class": "form-control"}),
            "primer_apellido": forms.TextInput(attrs={"class": "form-control"}),
            "segundo_apellido": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email_personal": forms.EmailInput(attrs={"class": "form-control"}),
            "eps": forms.TextInput(attrs={"class": "form-control"}),
            "fondo_pension": forms.TextInput(attrs={"class": "form-control"}),
            "fondo_cesantias": forms.TextInput(attrs={"class": "form-control"}),
            "caja_compensacion": forms.TextInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = [
            "empleado",
            "cargo",
            "tipo_contrato",
            "fecha_inicio",
            "fecha_fin",
            "salario_base",
            "auxilio_transporte",
            "activo",
        ]
        widgets = {
            "empleado": forms.Select(attrs={"class": "form-select"}),
            "cargo": forms.Select(attrs={"class": "form-select"}),
            "tipo_contrato": forms.Select(attrs={"class": "form-select"}),
            "fecha_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "salario_base": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "auxilio_transporte": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
