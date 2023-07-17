import os
import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models


def photo_path(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    chars = string.ascii_lowercase
    randomstring = ''.join((random.choice(chars)) for x in range(12))
    return f'avatars/{randomstring}{file_extension}'


class BaseUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)


class User(models.Model):
    user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(upload_to=photo_path)
    date_of_birth = models.DateField()
    manager_chat = models.OneToOneField(
        "chats.Chat", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
