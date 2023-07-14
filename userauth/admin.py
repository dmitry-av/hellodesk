from django.contrib import admin

from .models import BaseUser, User


admin.site.register(BaseUser)
admin.site.register(User)
