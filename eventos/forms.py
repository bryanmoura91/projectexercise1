from django import forms
from .models import Evento, Participante, Inscricao
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
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
        fields = ['nome', 'email', 'telefone', 'genero']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows':4, 'placeholder': 'Escreva seu feedback aqui...'}),
        }

class UserEmailPasswordForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    old_password = forms.CharField(label="Senha atual", widget=forms.PasswordInput, required=True)
    new_password1 = forms.CharField(label="Nova senha", widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label="Confirmação da nova senha", widget=forms.PasswordInput, required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['email'].initial = user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso por outro usuário.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if not self.user.check_password(old_password):
            raise forms.ValidationError("Senha atual incorreta.")

        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("As novas senhas não coincidem.")
            if len(new_password1) < 8:
                raise forms.ValidationError("A nova senha deve ter pelo menos 8 caracteres.")

        return cleaned_data

    def save(self):
        email = self.cleaned_data.get('email')
        new_password1 = self.cleaned_data.get('new_password1')

        if self.user.email != email:
            self.user.email = email
            self.user.save()

        if new_password1:
            self.user.set_password(new_password1)
            self.user.save()
