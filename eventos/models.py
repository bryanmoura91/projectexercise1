from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Informe o título do evento."
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Detalhes sobre o evento."
    )
    data = models.DateField(
        verbose_name="Data do evento"
    )
    local = models.CharField(
        max_length=200,
        verbose_name="Local do evento"
    )
    capacidade_maxima = models.PositiveIntegerField(
        verbose_name="Capacidade máxima de participantes"
    )
    banner = models.ImageField(
        upload_to='banners/' ,
        blank=True ,
        null=True ,
        verbose_name="Banner do evento"
    )
    criado_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='eventos',
        verbose_name="Criado por"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-data']

    def __str__(self):
        return f"{self.titulo} - {self.local}"


class Participante(models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome"
    )
    email = models.EmailField(
        verbose_name="E-mail"
    )
    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone"
    )
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    genero = models.CharField(
        max_length=1,
        choices=GENERO_CHOICES,
        verbose_name="Gênero",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Inscricao(models.Model):
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='inscricoes',
        verbose_name="Evento"
    )
    participante = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        related_name='inscricoes',
        verbose_name="Participante"
    )
    data_inscricao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da inscrição"
    )
    feedback = models.TextField(
        verbose_name="Feedback",
        blank=True,
        null=True,
        help_text="Mensagem de feedback do participante."
    )

    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"
        ordering = ['-data_inscricao']
        unique_together = ('evento', 'participante')  # evita duplicidade

    def __str__(self):
        return f"{self.participante.nome} inscrito em {self.evento.titulo}"
