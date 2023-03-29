from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .utils import check_if_superuser, unauthenticated_user

from django.contrib.auth.models import User

# Create your views here.
def landing(request):
    return render(request, 'landing.html')

@unauthenticated_user
def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if check_if_superuser(email=email):
                user = User.objects.create_superuser(username=username, email=email, password=password1)
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
        else:
            messages.error(request, 'As senhas não coincidem')

        messages.success(request, 'Conta criada com sucesso para ' + user.username)
        return redirect('login')
        
    return render(request, 'register.html')

@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            print('sim')
            login(request, user)
            return redirect('lobby')

        else:
            messages.info(request, 'E-mail ou senha incorretos')

    return render(request, 'login.html')

@login_required(login_url='login')
def lobby(request):
    return render(request, 'lobby.html')

@login_required(login_url='login')
def rooms(request):
    return render(request, 'rooms.html')

@login_required(login_url='login')
def chat(request):
    return render(request, 'chat.html')


@login_required(login_url='login')
def perfil(request):
    return render(request, 'perfil.html')

@login_required(login_url='login')
def deslogar_usuario(request):
    logout(request)
    return redirect('landing')


@login_required(login_url='login')
def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect('perfil')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha.html', {'form_senha': form_senha})
