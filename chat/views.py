from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from chat.forms import MessageForm
from .models import Announcement, Room, CATEGORIES
from django.contrib.auth.models import User
from .utils import unauthenticated_user


@unauthenticated_user
def landing(request):
    return render(request, "landing.html")


@login_required(login_url="/auth/login/")
def lobby(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "lobby.html", context)


@login_required(login_url="/auth/login/")
def rooms(request):
    return render(request, "rooms.html")


@login_required(login_url="/auth/login/")
def chat(request, room_id):
    announcements = Announcement.objects.all()[:4]
    form = MessageForm()
    context = {
        "room_name": room_id,
        "announcements": announcements,
        "form": form,
    }
    return render(request, "chat.html", context)


@login_required(login_url="/auth/login/")
def announcements_list(request, room_id):
    all_announcements = Announcement.objects.filter(room=room_id)
    context = {
        "announcements": all_announcements,
    }
    return render(request, "avisos.html", context)


@login_required(login_url="/auth/login/")
def criar_sala(request):
    categories = CATEGORIES
    if request.method == "POST":
        name = request.POST.get("nome", None)
        description = request.POST.get("descricao", None)
        category = request.POST.get("categoria", None)
        max_participants = request.POST.get("limite", None)
        new_room = Room(name=name, description=description, category=category, max_participants=max_participants)
        new_room.save()
        return redirect("/")
    context = {"categories": categories}
    return render(request, "criar_sala.html", context)
