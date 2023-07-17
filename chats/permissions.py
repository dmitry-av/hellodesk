from rest_framework.permissions import BasePermission
from django.shortcuts import render, get_object_or_404

from .models import Chat


class HasAccessToRoom(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and request.user.is_manager:
            return True
        chat_room = get_object_or_404(Chat, pk=view.kwargs['pk'])
        return chat_room.client == request.user
