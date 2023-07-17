from rest_framework import generics
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .serializers import RegistrationSerializer, BaseUserSerializer, UserSerializer
from .models import BaseUser, User


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class UserDetailAPI(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        baseuser = BaseUser.objects.get(pk=pk)
        if baseuser != request.user and not request.user.is_superuser and not request.user.is_staff and not request.user.is_manager:
            raise PermissionDenied(
                "You don't have permission to access this resource.")
        user = User.objects.get(user=baseuser)
        serializer = self.serializer_class(user, context={'request': request})
        return Response(serializer.data)

    def get_permissions(self):
        return super().get_permissions()
