from rest_framework import permissions


class ObjectAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.client or
            request.user.is_manager or
            request.user.is_superuser
        )
