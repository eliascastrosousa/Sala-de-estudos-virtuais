from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .utils import check_if_superuser, unauthenticated_user
from django.contrib.auth.models import User
from django.http import HttpResponse
import string 
import random
import time
import pyotp
import win32com.client as win32
import smtplib
import email.message

@unauthenticated_user
def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            registration_data = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'password1': password1,
                'codigoenviado': 1234 #dps automatizar o codigo 
            }
        
            request.session['registration_data'] = registration_data
            return redirect('register2')
        
        else:
            messages.error(request, 'As senhas não coincidem')
    return render(request, 'register.html')

def register2(request):
    if request.method == "POST":
        registration_data = request.session.get('registration_data', None) #traz os dados salvo na session

        if registration_data is not None:
            print('não esta vazio', registration_data('first_name'))
            
            codigorecebido = request.POST.get('codigoautenticacao')
            codigoenviado = registration_data.get('codigoenviado')

            if codigorecebido == codigoenviado:
                
                if check_if_superuser(email=registration_data.get('email')):
                    user = User.objects.create_superuser(
                        first_name = registration_data.get('first_name'),
                        last_name = registration_data.get('last_name'),
                        username = registration_data.get('username'), 
                        email = registration_data.get('email'),
                        password = registration_data.get('password1'))
                else:
                    user = User.objects.create_user(
                        first_name = registration_data.get('first_name'),
                        last_name = registration_data.get('last_name'),
                        username = registration_data.get('username'), 
                        email = registration_data.get('email'),
                        password = registration_data.get('password1'))
                
                
                messages.success(request, 'Conta criada com sucesso para ' + user.username)
                return redirect('login')

            messages.error(request, 'Os codigos não coincidem')
            
        else: 
            messages.error(request, 'Nenhum dado de usuario recebido')
            print('esta vazio')

    if 'registration_data' in request.session:
                    del request.session['registration_data']

    return render(request, 'register2.html')

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

@login_required(login_url="/auth/login/")
def perfil(request):
    return render(request, 'perfil.html')

@login_required(login_url="/auth/login/")
def deslogar_usuario(request):
    logout(request)
    return redirect('landing')


@login_required(login_url="/auth/login/")
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
