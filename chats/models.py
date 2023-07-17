from django.db import models
from django.contrib.auth import get_user_model
from userauth.models import User
from tickets.models import Ticket


class Chat(models.Model):
    ticket = models.OneToOneField(
        Ticket, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.ticket:
            return f"Chat for {self.ticket}"
        return f"Chat for {self.client.user}"


class Message(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
