from django import forms
from .models import Evento, Participante
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']