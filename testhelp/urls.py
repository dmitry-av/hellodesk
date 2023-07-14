from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from userauth.views import RegisterUserAPIView, UserDetailAPI
from tickets.views import TicketViewSet
from chats.views import ChatViewSet


router = routers.DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'chats', ChatViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterUserAPIView.as_view()),
    path('api/users/<int:pk>/', UserDetailAPI.as_view(), name='user-detail'),
]

urlpatterns += [path("api/auth/", TokenObtainPairView.as_view(),
                     name="jwt_obtain_pair"),
                path("api/auth/refresh/", TokenRefreshView.as_view(),
                     name="jwt_refresh"),
                ]
