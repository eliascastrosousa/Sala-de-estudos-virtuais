from django.shortcuts import redirect
from .models import Room


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("lobby")

        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def check_if_user_can_join(user, room_id):
    room = Room.objects.get(id=room_id)
    if room.members.filter(id=user.id).exists():
        return True
    elif room.members.count() >= room.max_participants:
        return False
    else:
        room.members.add(user)
        room.max_participants += 1
        return True
