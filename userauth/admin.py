from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import BaseUser, User
from django.contrib.auth.admin import UserAdmin


class EmployeeAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name',
         'last_name', 'email', 'is_manager')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'manager_chat_link', 'manager')

    def manager_chat_link(self, obj):
        chat = obj.manager_chat
        if chat:
            chat_url = reverse('chat-room', args=[chat.id])
            return format_html('<a href="{}">{}</a>', chat_url, chat_url)
        return None

    manager_chat_link.short_description = 'Manager Chat'

    def manager(self, obj):
        chat = obj.manager_chat
        if chat:
            return chat.manager.username


admin.site.register(BaseUser, EmployeeAdmin)
admin.site.register(User, ClientAdmin)
