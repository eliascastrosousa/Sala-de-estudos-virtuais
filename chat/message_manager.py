import os
import json
from .firebase import database

NUMBER_MESSAGES_THRESHOLD = 10
NUMBER_MESSAGES_TO_SAVE = 5
NUMBER_MESSAGES_TO_KEEP = 5


class Message:
    def __init__(self, text, sender, time, date, room):
        self.text = text
        self.sender = sender
        self.time = time
        self.date = date
        self.room = room


def append_message_to_json(message, room_id):
    message_data = {
        "text": message.text,
        "sender": message.sender,
        "time": message.time,
        "date": message.date,
        "room": room_id,
    }

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stored_messages", f"room{room_id}.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    else:
        data = []

    data.append(message_data)

    num_messages = len(data)
    print(num_messages)

    if num_messages >= NUMBER_MESSAGES_THRESHOLD:
        messages_to_save = data[:NUMBER_MESSAGES_TO_SAVE]

        # Push the older messages to the database
        for message in messages_to_save:
            database.child("room" + room_id).push(message)

        # Keep the recent messages in the JSON file
        data = data[-NUMBER_MESSAGES_TO_KEEP:]

        # Clear the JSON file
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)

        print(f"{NUMBER_MESSAGES_TO_SAVE} older messages saved to the database.")
        print(f"{NUMBER_MESSAGES_TO_KEEP} recent messages kept in the JSON file.")

    with open(file_path, "w") as json_file:
        json.dump(data, json_file)


def retrieve_messages_from_json(room_id):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stored_messages", f"room{room_id}.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return data
    else:
        return []


def retrieve_messages_from_firebase(room_id):
    messages_objects = database.child("room" + room_id).get()
    messages = [message.val() for message in messages_objects.each()]
    print(messages)
    return messages


def delete_messages_from_json(room_id):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stored_messages", f"room{room_id}.json")
    os.remove(file_path)


def delete_messages_from_firebase(room_id):
    database.child("room" + room_id).remove()
