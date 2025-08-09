from .forms import RegistrationForm, EventoForm, ParticipanteForm, FeedbackForm, UserEmailPasswordForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Evento, Participante, Inscricao

class EventoOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        evento = self.get_object()
        return evento.criado_por == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Você não tem permissão para realizar essa ação.")
        return redirect('evento-list')

class EventoListView(ListView):
    model = Evento
    template_name = 'eventos/evento_list.html'
    context_object_name = 'eventos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class EventoCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, "Evento criado com sucesso.")
        return super().form_valid(form)

class EventoUpdateView(LoginRequiredMixin, EventoOwnerMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento-list')

    def form_valid(self, form):
        messages.success(self.request, "Evento atualizado com sucesso.")
        return super().form_valid(form)

class EventoDeleteView(LoginRequiredMixin, EventoOwnerMixin, DeleteView):
    model = Evento
    template_name = 'eventos/evento_confirm_delete.html'
    success_url = reverse_lazy('evento-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Evento deletado com sucesso.")
        return super().delete(request, *args, **kwargs)

class InscricaoCreateView(View):
    def get(self, request, evento_id):
        evento = get_object_or_404(Evento, id=evento_id)

        if request.user.is_authenticated and evento.criado_por == request.user:
            messages.error(request, "Você é o promotor deste evento e não pode se inscrever.")
            return redirect('evento-list')

        if evento.inscricoes.count() >= evento.capacidade_maxima:
            messages.error(request, "Capacidade máxima atingida para este evento.")
            return redirect('evento-list')

        form = ParticipanteForm()
        return render(request, 'eventos/inscricao_form.html', {'form': form, 'evento': evento})

    def post(self, request, evento_id):
        evento = get_object_or_404(Evento, id=evento_id)

        if request.user.is_authenticated and evento.criado_por == request.user:
            messages.error(request, "Você é o promotor deste evento e não pode se inscrever.")
            return redirect('evento-list')

        if evento.inscricoes.count() >= evento.capacidade_maxima:
            messages.error(request, "Capacidade máxima atingida para este evento.")
            return redirect('evento-list')

        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save()
            Inscricao.objects.create(evento=evento, participante=participante)
            messages.success(request, "Inscrição realizada com sucesso.")
            messages.info(request, "Um e-mail de confirmação foi enviado (simulação).")
            return redirect('evento-list')
        return render(request, 'eventos/inscricao_form.html', {'form': form, 'evento': evento})

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário registrado com sucesso.")
            return redirect('login')
        return render(request, 'registration/register.html', {'form': form})

class ParticipantesListView(LoginRequiredMixin, ListView):
    model = Inscricao
    template_name = 'eventos/participantes_list.html'
    context_object_name = 'inscricoes'

    def get_queryset(self):
        return Inscricao.objects.filter(evento__criado_por=self.request.user).select_related('participante', 'evento')

@method_decorator(login_required, name='dispatch')
class UserEditView(View):
    def get(self, request):
        form = UserEmailPasswordForm(user=request.user)
        return render(request, 'registration/user_edit.html', {'form': form})

    def post(self, request):
        form = UserEmailPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Email e/ou senha atualizados com sucesso.")
            return redirect('user-edit')
        messages.error(request, "Erro ao atualizar email e/ou senha.")
        return render(request, 'registration/user_edit.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class FeedbackCreateView(View):
    def get(self, request, inscricao_id):
        inscricao = get_object_or_404(Inscricao, id=inscricao_id, participante__email=request.user.email)
        form = FeedbackForm(instance=inscricao)
        return render(request, 'eventos/feedback_form.html', {'form': form, 'inscricao': inscricao})

    def post(self, request, inscricao_id):
        inscricao = get_object_or_404(Inscricao, id=inscricao_id, participante__email=request.user.email)
        form = FeedbackForm(request.POST, instance=inscricao)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback enviado com sucesso.")
            return redirect('evento-list')
        return render(request, 'eventos/feedback_form.html', {'form': form, 'inscricao': inscricao})
