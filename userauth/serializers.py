import random
from rest_framework import serializers
from rest_framework.reverse import reverse

from chats.models import Chat

from .models import BaseUser, User


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ["id", "username", "email",
                  "first_name", "last_name",  "is_manager"]
        read_only_field = ["created", "updated"]


class UserSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()
    manager_chat = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('user', 'avatar', 'date_of_birth', 'manager_chat')

    def get_manager_chat(self, user):
        chat = user.manager_chat
        if chat:
            request = self.context.get('request')
            chat_url = reverse(
                'chat-websocket', urlconf='chats.routing', args=[chat.pk], request=request)
            websocket_url = chat_url.replace('http', 'ws', 1)
            return websocket_url
        return None


class RegistrationSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(write_only=True, required=False)
    date_of_birth = serializers.DateField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = BaseUser
        fields = ('id', 'username', 'password', 'email', 'first_name',
                  'last_name', 'avatar', 'date_of_birth')

    def create(self, validated_data):
        baseuser = BaseUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        baseuser.set_password(validated_data['password'])
        baseuser.save()
        user = User.objects.create(
            user=baseuser, avatar=validated_data['avatar'], date_of_birth=validated_data['date_of_birth'])
        manager_users = BaseUser.objects.filter(is_manager=True)
        if manager_users.exists():
            manager = random.choice(manager_users)
        else:
            manager = None
        user.manager_chat = Chat.objects.create(client=user, manager=manager)
        user.save()
        return baseuser
