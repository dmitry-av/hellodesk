from django.db import models
from django.contrib.auth import get_user_model

from tickets.models import Ticket

User = get_user_model()


class Chat(models.Model):
    ticket = models.OneToOneField(
        Ticket, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.ticket:
            return f"Chat for {self.ticket}"
        return f"Chat for {self.client}"
