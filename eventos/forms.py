from django import forms
from .models import Evento, Participante

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descricao', 'data', 'local', 'capacidade_maxima', 'banner']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'email', 'telefone', 'dados_adicionais']
