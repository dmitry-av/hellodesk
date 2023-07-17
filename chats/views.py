from rest_framework import viewsets
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404


from chats.models import Chat
from chats.permissions import HasAccessToRoom
from .serializers import ChatSerializer
from tickets.permissions import ObjectAccessPermission


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [ObjectAccessPermission]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, ObjectAccessPermission]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class RoomView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'chats/room.html'
    permission_classes = [HasAccessToRoom]

    def get(self, request, pk):
        chat_room = get_object_or_404(Chat, pk=pk)
        return Response({'room': chat_room})
