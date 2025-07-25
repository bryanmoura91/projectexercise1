from django.contrib import admin
from django.urls import path
from eventos.views import (
    EventoListView,
    EventoCreateView,
    EventoUpdateView,
    EventoDeleteView,
    InscricaoCreateView
)
from django.contrib.auth.views import LoginView, LogoutView

# 👇 IMPORTANTE: essas duas linhas para arquivos de mídia
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticação
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Listagem de eventos
    path('', EventoListView.as_view(), name='evento-list'),

    # CRUD de eventos
    path('evento/novo/', EventoCreateView.as_view(), name='evento-create'),
    path('evento/<int:pk>/editar/', EventoUpdateView.as_view(), name='evento-update'),
    path('evento/<int:pk>/deletar/', EventoDeleteView.as_view(), name='evento-delete'),

    # Inscrição em evento
    path('evento/<int:evento_id>/inscricao/', InscricaoCreateView.as_view(), name='evento-inscricao'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
