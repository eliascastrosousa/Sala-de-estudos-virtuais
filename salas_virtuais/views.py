from django.shortcuts import render, redirect
from .models import Sala
from .models import CATEGORIAS
from datetime import datetime

# Create your views here.
def index(request):
    salas = Sala.objects.all().order_by('-data_criacao')
    context = {'salas': salas}
    return render(request, 'index.html', context)

def criar_sala(request):
    categorias = CATEGORIAS
    if request.method == 'POST':
        nome = request.POST.get('nome', None)
        descricao = request.POST.get('descricao', None)
        categoria = request.POST.get('categoria', None)
        limite_participantes = request.POST.get('limite', 50)
        nova_sala = Sala(nome=nome, descricao=descricao, categoria=categoria,limite_participantes=limite_participantes)
        nova_sala.save()
        return redirect('/')
    context = {'categorias': categorias}
    return render(request, 'criar_sala.html', context)

def editar_sala(request, pk):
    sala = Sala.objects.get(id=pk)
    categorias = CATEGORIAS
    if request.method == 'POST':
        nome = request.POST.get('nome', None)
        descricao = request.POST.get('descricao', None)
        categoria = request.POST.get('categoria', None)
        limite_participantes = request.POST.get('limite', None)
        nova_sala = Sala(id=pk, nome=nome, descricao=descricao, categoria=categoria,limite_participantes=limite_participantes, data_criacao=datetime.now())
        nova_sala.save()
        return redirect('/')
    context = {'sala': sala, 'categorias': categorias}
    return render(request, 'editar_sala.html', context)

def excluir_sala(request, pk):
    sala = Sala.objects.get(id=pk)
    if request.method == 'POST':
        sala.delete()
        return redirect('/')
    context = {'sala': sala}
    return render(request, 'excluir_sala.html', context)