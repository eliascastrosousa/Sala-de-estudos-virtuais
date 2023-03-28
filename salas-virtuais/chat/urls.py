from django.urls import path
from .views import *

urlpatterns = [
    path('', landing, name='landing'),
    path('login', login_page, name='login'),
    path('register', register_page, name='register'),
    path('lobby', lobby, name='lobby'),
    path('rooms', rooms, name='rooms'),
    path('chat', chat, name='chat'),
    path('perfil', perfil, name='perfil'),
]
