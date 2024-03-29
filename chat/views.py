from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from chat.forms import DocumentForm, RoadmapForm
from .models import Announcement, Room, Category, Roadmap, Document
from .filters import RoomFilter
from .utils import check_if_user_can_join
from .message_manager import (
    delete_messages_from_firebase,
    delete_messages_from_json,
    retrieve_messages_from_json,
    retrieve_messages_from_firebase,
)


@login_required(login_url="/login/")
def lobby(request):
    room_filter = RoomFilter(request.GET, queryset=Room.objects.all())
    context = {
        "room_filter": room_filter,
    }
    return render(request, "lobby.html", context)


@login_required(login_url="/login/")
def rooms(request):
    user = request.user
    user_rooms = Room.objects.filter(members__in=[user])
    context = {
        "user_rooms": user_rooms,
    }
    return render(request, "rooms.html", context)


@login_required(login_url="/login/")
def chat(request, room_id):
    if not check_if_user_can_join(request.user, room_id):
        messages.error(request, "A sala já atingiu seu limite máximo")
        return render(request, "lobby.html")
    else:
        chat_messages = retrieve_messages_from_json(room_id)
        announcements = Announcement.objects.filter(room=room_id)[:7]
        roadmaps = Roadmap.objects.filter(room=room_id)[:4]
        context = {
            "room_id": room_id,
            "messages": chat_messages,
            "announcements": announcements,
            "roadmaps": roadmaps,
        }
        return render(request, "chat.html", context)


@login_required(login_url="/login/")
def all_messages(request, room_id):
    all_messages = retrieve_messages_from_firebase(room_id)
    context = {
        "room_id": room_id,
        "all_messages": all_messages,
    }
    return render(request, "mensagens.html", context)


@login_required(login_url="/login/")
def announcements_list(request, room_id):
    all_announcements = Announcement.objects.filter(room=room_id)
    context = {
        "announcements": all_announcements,
        "room_id": room_id,
    }
    return render(request, "avisos.html", context)


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def delete_announcement(request, room_id, announcement_id):
    if request.method == "POST":
        announcement = Announcement.objects.get(id=announcement_id)
        announcement.delete()
        return redirect(reverse("avisos", args=[room_id]))


@login_required(login_url="/login/")
def create_room(request):
    categories = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("nome", None)
        description = request.POST.get("descricao", None)
        category_input = request.POST.get("categoria", None)
        category = Category.objects.get(name=category_input)
        max_participants = request.POST.get("limite", None)
        image = request.FILES.get("imagem")
        new_room = Room(
            name=name, description=description, category=category, max_participants=max_participants, image=image
        )
        new_room.save()
        return redirect("/")
    context = {"categories": categories}
    return render(request, "criar_sala.html", context)


@login_required(login_url="/login/")
def edit_room(request, room_id):
    categories = Category.objects.all()
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        name = request.POST.get("nome", None)
        description = request.POST.get("descricao", None)
        category_input = request.POST.get("categoria", None)
        category = Category.objects.get(name=category_input)
        image = request.FILES.get("imagem")
        room.name = name
        room.description = description
        room.category = category
        if image:
            room.image = image
        room.save()
        return redirect("/")
    context = {
        "room": room,
        "categories": categories,
    }
    return render(request, "editar_sala.html", context)


@login_required(login_url="/login/")
def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    room.delete()
    delete_messages_from_json(room_id)
    delete_messages_from_firebase(room_id)
    return redirect("/")


@login_required(login_url="/login/")
def roadmap(request, room_id, roadmap_id):
    roadmap = Roadmap.objects.get(id=roadmap_id)
    context = {
        "room_id": room_id,
        "roadmap": roadmap,
    }
    return render(request, "roadmap.html", context)


@login_required(login_url="/login/")
def all_roadmaps(request, room_id):
    roadmaps = Roadmap.objects.filter(room=room_id).order_by("-created")
    form = DocumentForm()
    context = {
        "room_id": room_id,
        "roadmaps": roadmaps,
        "form": form,
    }
    return render(request, "roadmaps.html", context)


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def delete_roadmap(request, room_id, roadmap_id):
    roadmap = Roadmap.objects.get(id=roadmap_id)
    roadmap.delete()
    return redirect(reverse("roadmaps", args=[room_id]))


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def delete_document(request, room_id, document_id):
    document = Document.objects.get(id=document_id)
    document.delete()
    return redirect(reverse("roadmaps", args=[room_id]))


@login_required(login_url="/login/")
def create_category(request):
    categories = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name", None)
        Category.objects.create(name=name)
        return redirect("criar_sala")
    context = {
        "categories": categories,
    }
    return render(request, "adicionar_categoria.html", context)


@login_required(login_url="/login/")
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    previous_url = request.META.get("HTTP_REFERER")
    return redirect(previous_url)
