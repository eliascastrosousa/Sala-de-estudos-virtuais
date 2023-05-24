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

        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 4)) 
        chave_mestra = str(res)
        codigo = pyotp.TOTP(chave_mestra)

        if password1 == password2:

            registration_data = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'password1': password1,
                'codigoenviado': codigo.now()
            }
        
            request.session['registration_data'] = registration_data
            print("page register 1")
            print(registration_data)
            print(request.session['registration_data'])
            print("------------")

            return redirect('register2')
        
        else:
            messages.error(request, 'As senhas não coincidem')
    return render(request, 'register.html')

@unauthenticated_user
def register2(request):
    if request.method == "POST":
        registration_data = request.session.get('registration_data', None) #traz os dados salvo na session
        if registration_data is not None:
            codigorecebido = request.POST['codigoautenticacao']

            first_name = registration_data.get('first_name')
            last_name = registration_data.get('last_name')
            username = registration_data.get('username')
            email = registration_data.get('email')
            password = registration_data.get('password1')
            codigoenviado = registration_data.get('codigoenviado')
            print("register 2 dados salvos em variavel")
            print("nome do usuario: "+ first_name, last_name, username, email, password, codigoenviado)
            print(registration_data)
            print(request.session['registration_data'])

            print(codigorecebido,codigoenviado)
            print(type(codigorecebido))
            print(type(codigoenviado))

            
            if str(codigorecebido) == str(codigoenviado):
                print(codigorecebido , codigoenviado)
                    
                if check_if_superuser(email=email):
                    user = User.objects.create_superuser(
                        first_name = first_name,
                        last_name = last_name,
                        username = str(username), 
                        email = email,
                        password = password)
                    print("\nconta criada superuser")
                        
                else:
                    user = User.objects.create_user(
                        first_name = first_name,
                        last_name = last_name,
                        username = str(username), 
                        email = email,
                        password = password)
                    print("\nconta criada user padrao")
            
                messages.success(request, 'Conta criada com sucesso ')
                print(codigorecebido , codigoenviado)
                return redirect('login')
            else: 
                print(codigorecebido,codigoenviado)
                messages.error(request, 'Os codigos não coincidem')

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
            messages.info(request, 'Username ou senha incorretos')

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
