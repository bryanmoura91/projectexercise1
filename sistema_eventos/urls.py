from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from eventos.views import (
    EventoListView,
    EventoCreateView,
    EventoUpdateView,
    EventoDeleteView,
    InscricaoCreateView,
    RegisterView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticação
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # Eventos
    path('', EventoListView.as_view(), name='evento-list'),
    path('evento/novo/', EventoCreateView.as_view(), name='evento-create'),
    path('evento/<int:pk>/editar/', EventoUpdateView.as_view(), name='evento-update'),
    path('evento/<int:pk>/deletar/', EventoDeleteView.as_view(), name='evento-delete'),

    # Inscrição
    path('evento/<int:evento_id>/inscricao/', InscricaoCreateView.as_view(), name='evento-inscricao'),
]

# Arquivos de mídia em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
