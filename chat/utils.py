from django.shortcuts import redirect
import os
import json
from .models import Room


class Message:
    def __init__(self, text, sender, time, date, room):
        self.text = text
        self.sender = sender
        self.time = time
        self.date = date
        self.room = room


def append_message_to_json(message, room_id):
    message_data = {
        "message": {
            "text": message.text,
            "sender": message.sender,
            "time": message.time,
            "date": message.date,
            "room": room_id,
        }
    }

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stored_messages", f"room{room_id}.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    else:
        data = []

    data.append(message_data)
    print(len(data))

    with open(file_path, "w") as json_file:
        json.dump(data, json_file)


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
