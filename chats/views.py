from rest_framework import viewsets
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import serializers


from chats.models import Chat
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
