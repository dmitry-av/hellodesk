# Generated by Django 4.2.3 on 2023-07-15 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("userauth", "0004_user_manager_chat"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chats", "0002_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="manager",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="chat",
            name="client",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="userauth.user"
            ),
        ),
    ]
