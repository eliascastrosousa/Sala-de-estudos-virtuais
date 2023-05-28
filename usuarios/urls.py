from . import views
from django.urls import path
from .views import *


urlpatterns = [
    path('register', views.register_page, name='register' ),
    path('register2', views.register2, name='register2' ),
    path('login', views.login_page, name='login' ),
    path('perfil', perfil, name='perfil'),
    path('alterar_senha', alterar_senha, name='alterar_senha'),
    path('deslogar_usuario', deslogar_usuario, name='deslogar_usuario')
]