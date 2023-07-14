from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import serializers

from .models import Category, Ticket
from chats.models import Chat
from .serializers import TicketSerializer
from .permissions import ObjectAccessPermission


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, ObjectAccessPermission]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        category_name = self.request.data.get('category', {}).get('name')
        category = Category.objects.get(name=category_name)
        serializer.validated_data['category'] = category
        subject = serializer.validated_data['subject']
        user = self.request.user
        if Ticket.objects.filter(subject=subject, client=user).exists():
            raise serializers.ValidationError(
                "A ticket with the same subject already exists for the user.")
        ticket = serializer.save(client=user)
        Chat.objects.create(ticket=ticket, client=user)
