from . import views
from django.urls import path
from .views import landing, register, register2, alterar_senha, deslogar_usuario, perfil, login


urlpatterns = [
    path("", landing, name="landing"),
    path("register", views.register, name="register"),
    path("register2", views.register2, name="register2"),
    path("login", views.login, name="login"),
    path("perfil", perfil, name="perfil"),
    path("alterar_senha", alterar_senha, name="alterar_senha"),
    path("deslogar_usuario", deslogar_usuario, name="deslogar_usuario"),
]
