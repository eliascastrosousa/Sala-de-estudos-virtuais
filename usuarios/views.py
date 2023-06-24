from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_django, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .utils import check_if_superuser, unauthenticated_user
from django.contrib.auth.models import User
import string
import random
import pyotp
import smtplib
import email.message
import smtplib
import email.message


@unauthenticated_user
def landing(request):
    return render(request, "landing.html", context)


def enviar_email(first_name, emailusuario, codigo):
    print(first_name, emailusuario, codigo)
    corpo_email = (
        """
            <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Codigo para Autenticação</title>
        </head>
        <body>
        <!-- email_autenticacao.html -->
        <h1>Olá , """
        + str(first_name)
        + """</h1>
        <hr>
        <h2>Recebemos a solicitação de codigo para conclusão do cadastro de usuario em Sala de Estudos.</h2>
		<br>
        <h2>Codigo:<strong> """
        + str(codigo.now())
        + """</strong> </h2>
		<br>

        <h2>Para concluir o seu perfil, utilize o codigo acima.</h2>
        <h2>Obrigado por nos ajudar a manter sua conta segura.</h2>
		-----
        <h3>Atenciosamente</h3>
        <h3>A equipe da Sala de Estudos Virtuais</h3>

        </body>
        </html>
    """
    )
    print(str(emailusuario))
    print(str(corpo_email))

    msg = email.message.Message()
    msg["Subject"] = "Seu codigo de uso único"
    msg["From"] = "sala.de.estudos.ifsp@gmail.com"
    msg["To"] = str(emailusuario)
    password = "nohsxnlerpfdpyqy"
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(corpo_email)

    s = smtplib.SMTP("smtp.gmail.com: 587")
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg["From"], password)
    s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))
    print("Email enviado")


@unauthenticated_user
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        res = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
        chave_mestra = str(res)
        codigo = pyotp.TOTP(chave_mestra)

        if password1 == password2:
            registration_data = {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "email": email,
                "password1": password1,
                "codigoenviado": codigo.now(),
            }

            request.session["registration_data"] = registration_data
            print("page register 1")
            print(registration_data)
            print(request.session["registration_data"])
            print("------------")
            emailusuario = email
            enviar_email(first_name, emailusuario, codigo)

            return redirect("register2")
        else:
            messages.error(request, "As senhas não coincidem")
    return render(request, "register.html")


@unauthenticated_user
def register2(request):
    if request.method == "POST":
        registration_data = request.session.get("registration_data", None)  # traz os dados salvo na session
        if registration_data is not None:
            codigorecebido = request.POST["codigoautenticacao"]

            first_name = registration_data.get("first_name")
            last_name = registration_data.get("last_name")
            username = registration_data.get("username")
            email = registration_data.get("email")
            password = registration_data.get("password1")
            codigoenviado = registration_data.get("codigoenviado")
            print("register 2 dados salvos em variavel")
            print("nome do usuario: " + first_name, last_name, username, email, password, codigoenviado)
            print(registration_data)
            print(request.session["registration_data"])

            print(codigorecebido, codigoenviado)
            print(type(codigorecebido))
            print(type(codigoenviado))

            if str(codigorecebido) == str(codigoenviado):
                print(codigorecebido, codigoenviado)

                if check_if_superuser(email=email):
                    user = User.objects.create_superuser(
                        first_name=first_name,
                        last_name=last_name,
                        username=str(username),
                        email=email,
                        password=password,
                    )
                    print("\nconta criada superuser")

                else:
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=str(username),
                        email=email,
                        password=password,
                    )
                    print("\nconta criada user padrao")

                messages.success(request, "Conta criada com sucesso para " + username)
                print(codigorecebido, codigoenviado)
                return redirect("login")
            else:
                print(codigorecebido, codigoenviado)
                messages.error(request, "Os codigos não coincidem")

        if "registration_data" in request.session:
            del request.session["registration_data"]

    return render(request, "register2.html")


@unauthenticated_user
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login_django(request, user)
            return redirect("lobby")
        else:
            return render(request, "login.html", {"error": "Username ou senha invalidos."})


@login_required(login_url="/auth/login/")
def perfil(request):
    return render(request, "perfil.html")


@login_required(login_url="/auth/login/")
def deslogar_usuario(request):
    logout(request)
    return redirect("landing")


@login_required(login_url="/auth/login/")
def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect("perfil")
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, "alterar_senha.html", {"form_senha": form_senha})
