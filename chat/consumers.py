import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime
from .message_manager import Message, append_message_to_json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["room_name"]

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json["text"]
        sender = text_data_json["sender"]
        room = text_data_json["room"]
        time = datetime.now().strftime("%H:%M")
        date = datetime.now().strftime("%d-%m-%Y")

        message = Message(text=text, sender=sender, time=time, date=date, room=room)
        append_message_to_json(message, room)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "text": text,
                "sender": sender,
                "room": room,
                "time": time,
                "date": date,
            },
        )

    def chat_message(self, event):
        text = event["text"]
        sender = event["sender"]
        time = event["time"]

        self.send(text_data=json.dumps({"type": "chat", "text": text, "sender": sender, "time": time}))
