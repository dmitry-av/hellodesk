from rest_framework import serializers

from .models import BaseUser, User


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ["id", "username", "email",
                  "first_name", "last_name",  "is_manager"]
        read_only_field = ["created", "updated"]


class UserSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = User
        fields = ('user', 'avatar', 'date_of_birth')


class RegistrationSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(write_only=True, required=False)
    date_of_birth = serializers.DateField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = BaseUser
        fields = ('username', 'password', 'email', 'first_name',
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
        User.objects.create(
            user=baseuser, avatar=validated_data['avatar'], date_of_birth=validated_data['date_of_birth'])
        return baseuser
