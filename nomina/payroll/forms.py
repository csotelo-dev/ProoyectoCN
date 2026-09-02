"""Formularios del módulo Payroll."""

from django import forms

from .models import Novedad, ParametroNomina, PeriodoNomina


class ParametroNominaForm(forms.ModelForm):
    class Meta:
        model = ParametroNomina
        fields = "__all__"
        widgets = {field: forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}) for field in [
            "smmlv", "auxilio_transporte", "porcentaje_salud_empleado",
            "porcentaje_salud_empleador", "porcentaje_pension_empleado",
            "porcentaje_pension_empleador", "porcentaje_arl_base",
            "porcentaje_sena", "porcentaje_icbf", "porcentaje_caja_compensacion",
        ]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["anio"].widget = forms.NumberInput(attrs={"class": "form-control"})
        self.fields["tope_auxilio_transporte_smmlv"].widget = forms.NumberInput(attrs={"class": "form-control"})


class PeriodoNominaForm(forms.ModelForm):
    class Meta:
        model = PeriodoNomina
        fields = ["nombre", "fecha_inicio", "fecha_fin", "parametros"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "parametros": forms.Select(attrs={"class": "form-select"}),
        }


class NovedadForm(forms.ModelForm):
    class Meta:
        model = Novedad
        fields = ["periodo", "empleado", "tipo", "cantidad", "valor", "observacion"]
        widgets = {
            "periodo": forms.Select(attrs={"class": "form-select"}),
            "empleado": forms.Select(attrs={"class": "form-select"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "observacion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
