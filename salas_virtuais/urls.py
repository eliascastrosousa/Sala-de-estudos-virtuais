from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('criar_sala/', criar_sala, name='criar_sala'),
    path('editar_sala/<int:pk>/', editar_sala, name='editar_sala'),
    path('excluir_sala/<int:pk>/', excluir_sala, name='excluir_sala'),
]
