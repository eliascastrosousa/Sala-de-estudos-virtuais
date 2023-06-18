from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from chat.forms import DocumentForm, MessageForm, RoadmapForm
from .models import Announcement, Room, CATEGORIES, Roadmap, Document
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
    announcements = Announcement.objects.filter(room=room_id)[:4]
    roadmaps = Roadmap.objects.filter(room=room_id)[:4]
    form = MessageForm()
    context = {
        "room_id": room_id,
        "announcements": announcements,
        "roadmaps": roadmaps,
        "form": form,
    }
    return render(request, "chat.html", context)


@login_required(login_url="/auth/login/")
def announcements_list(request, room_id):
    all_announcements = Announcement.objects.filter(room=room_id)
    context = {
        "announcements": all_announcements,
        "room_id": room_id,
    }
    return render(request, "avisos.html", context)


@login_required(login_url="/auth/login/")
def create_announcement(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == "POST":
        title = request.POST.get("titulo", None)
        description = request.POST.get("descricao", None)
        new_annoucement = Announcement(title=title, description=description, created_by=request.user, room=room)
        new_annoucement.save()
        return redirect(reverse("avisos", args=[room_id]))
    context = {"room_id": room_id}
    return render(request, "criar_aviso.html", context)


@login_required(login_url="/auth/login/")
def edit_announcement(request, room_id, announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)
    if request.method == "POST":
        title = request.POST.get("titulo", None)
        description = request.POST.get("descricao", None)
        announcement.title = title
        announcement.description = description
        announcement.save()
        return redirect(reverse("avisos", args=[room_id]))
    context = {
        "room_id": room_id,
        "announcement": announcement,
    }
    return render(request, "editar_aviso.html", context)


@login_required(login_url="/auth/login/")
def delete_announcement(request, room_id, announcement_id):
    if request.method == "POST":
        announcement = Announcement.objects.get(id=announcement_id)
        print(announcement)
        print(room_id)
        announcement.delete()
        return redirect(reverse("avisos", args=[room_id]))


@login_required(login_url="/auth/login/")
def create_room(request):
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


@login_required(login_url="/auth/login/")
def roadmap(request, room_id, roadmap_id):
    roadmap = Roadmap.objects.get(id=roadmap_id)
    context = {
        "room_id": room_id,
        "roadmap": roadmap,
    }
    return render(request, "roadmap.html", context)


@login_required(login_url="/auth/login/")
def all_roadmaps(request, room_id):
    roadmaps = Roadmap.objects.filter(room=room_id).order_by("-created")
    form = DocumentForm()
    context = {
        "room_id": room_id,
        "roadmaps": roadmaps,
        "form": form,
    }
    return render(request, "roadmaps.html", context)


@login_required(login_url="/auth/login/")
def create_roadmap(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == "POST":
        form = RoadmapForm(request.POST)
        if form.is_valid():
            my_form_data = form.save(commit=False)
            my_form_data.created_by = request.user
            my_form_data.room = room
            my_form_data.save()
            return redirect(reverse("roadmaps", args=[room_id]))
    else:
        form = RoadmapForm()
    context = {
        "room_id": room_id,
        "form": form,
    }
    return render(request, "criar_roadmap.html", context)


@login_required(login_url="/auth/login/")
def edit_roadmap(request, room_id, roadmap_id):
    room = Room.objects.get(id=room_id)
    roadmap = Roadmap.objects.get(id=roadmap_id)
    if request.method == "POST":
        form = RoadmapForm(request.POST, instance=roadmap)
        if form.is_valid():
            my_form_data = form.save(commit=False)
            my_form_data.created_by = request.user
            my_form_data.room = room
            my_form_data.save()
            return redirect(reverse("roadmaps", args=[room_id]))
    else:
        form = RoadmapForm(instance=roadmap)
    context = {
        "room_id": room_id,
        "roadmap": roadmap,
        "form": form,
    }
    return render(request, "editar_roadmap.html", context)


@login_required(login_url="/auth/login/")
def delete_roadmap(request, room_id, roadmap_id):
    roadmap = Roadmap.objects.get(id=roadmap_id)
    roadmap.delete()
    return redirect(reverse("roadmaps", args=[room_id]))


@login_required(login_url="/auth/login/")
def create_document(request, room_id, roadmap_id):
    roadmap = Roadmap.objects.get(id=roadmap_id)
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.roadmap = roadmap
            document.save()
            return redirect(reverse("roadmaps", args=[room_id]))
    else:
        form = DocumentForm()
    roadmaps = Roadmap.objects.filter(room=room_id).order_by("-created")
    context = {
        "room_id": room_id,
        "roadmaps": roadmaps,
        "form": form,
    }
    return render(request, "roadmaps.html", context)


@login_required(login_url="/auth/login/")
def delete_document(request, room_id, document_id):
    document = Document.objects.get(id=document_id)
    document.delete()
    return redirect(reverse("roadmaps", args=[room_id]))
