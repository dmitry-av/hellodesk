import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import DenyConnection

from .models import Chat, Message


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.pk = None
        self.room_group_name = None
        self.room = None
        self.user = None

    def connect(self):
        self.pk = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_{self.pk}'
        self.room = Chat.objects.get(pk=self.pk)
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            raise DenyConnection("You are not authenticated.")

        if self.room.ticket:
            if (self.user != self.room.client.user and
                    not self.user.is_manager and
                    not self.user.is_superuser):
                raise DenyConnection(
                    "You are not authorized to access this chat.")
        else:
            if (self.user != self.room.client.user and
                    self.user != self.room.manager and
                    not self.user.is_superuser):
                raise DenyConnection(
                    "You are not authorized to access this chat.")
        # connection accepted
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        messages = Message.objects.filter(room=self.room)
        for message in messages:
            self.send_message_to_client(message)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user.username,
                'message': message,
            }
        )
        Message.objects.create(
            user=self.user, room=self.room, content=message)  # new

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def send_message_to_client(self, message):
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'user': message.user.username,
            'message': message.content,
        }))
