from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)
    sort_order = models.IntegerField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.TextField(max_length=200)
    details = models.TextField()
    client = models.ForeignKey(
        User, related_name="tickets", on_delete=models.CASCADE)

    def __str__(self):
        return self.subject
