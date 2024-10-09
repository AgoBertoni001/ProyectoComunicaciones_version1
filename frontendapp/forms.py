from django import forms
from .models import Planta

class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = ['imagen', 'estado', 'descripcion']
    