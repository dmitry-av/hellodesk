from rest_framework import serializers
from rest_framework.reverse import reverse

from chats.models import Chat
from .models import Ticket, Category
from userauth.serializers import BaseUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    client = BaseUserSerializer(read_only=True)
    chat = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ('subject', 'details', 'client', 'category', 'chat')

    def get_chat(self, ticket):
        chat = Chat.objects.get(ticket=ticket)
        if chat:
            request = self.context.get('request')
            chat_url = reverse(
                'chat-websocket', urlconf='chats.routing', args=[chat.pk], request=request)
            websocket_url = chat_url.replace('http', 'ws', 1)
            return websocket_url
        return None
