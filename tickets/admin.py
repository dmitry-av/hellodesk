from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Ticket, Category


class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'client', 'category', 'chat_link')

    def chat_link(self, obj):
        chat = obj.chat
        if chat:
            chat_url = reverse('chat-detail', args=[obj.chat.id])
            full_chat_url = self.admin_site.site_url + chat_url
            return format_html('<a href="{}">{}</a>', chat_url, chat_url)
        return None

    chat_link.short_description = 'Chat'


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Category)
