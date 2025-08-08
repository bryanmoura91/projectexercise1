
from .forms import RegistrationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

from .models import Evento, Participante, Inscricao
from .forms import EventoForm, ParticipanteForm

# 📌 Listar eventos
class EventoListView(ListView):
    model = Evento
    template_name = 'eventos/evento_list.html'
    context_object_name = 'eventos'


# 📌 Criar evento
class EventoCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


# 📌 Atualizar evento
class EventoUpdateView(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')


# 📌 Deletar evento
class EventoDeleteView(LoginRequiredMixin, DeleteView):
    model = Evento
    template_name = 'eventos/evento_confirm_delete.html'
    success_url = reverse_lazy('evento-list')


# 📌 Inscrição em evento
class InscricaoCreateView(View):
    def get(self, request, evento_id):
        form = ParticipanteForm()
        evento = get_object_or_404(Evento, id=evento_id)
        return render(request, 'eventos/inscricao_form.html', {'form': form, 'evento': evento})

    def post(self, request, evento_id):
        evento = get_object_or_404(Evento, id=evento_id)
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            if evento.inscricoes.count() >= evento.capacidade_maxima:
                return render(request, 'eventos/inscricao_form.html', {
                    'form': form,
                    'evento': evento,
                    'erro': 'Capacidade máxima atingida para este evento.'
                })
            participante = form.save()
            Inscricao.objects.create(evento=evento, participante=participante)
            return redirect('evento-list')
        return render(request, 'eventos/inscricao_form.html', {'form': form, 'evento': evento})


# 📌 Cadastro de usuário (deve estar fora das outras views!)
class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'registration/register.html', {'form': form})
