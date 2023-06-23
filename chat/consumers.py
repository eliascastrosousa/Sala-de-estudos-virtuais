import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime
from . import firebase


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["room_name"]

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room_id = text_data_json["room"]
        sent_time = datetime.now().strftime("%H:%M")
        sent_date = datetime.now().strftime("%d-%m-%Y")

        # Store in non-relational database here

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "room": room_id,
                "sent_time": sent_time,
                "sent_date": sent_date,
            },
        )

    def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        sent_time = event["sent_time"]

        self.send(text_data=json.dumps({"type": "chat", "message": message, "username": username, "sent": sent_time}))
