from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from userauth.views import RegisterUserAPIView, UserDetailAPI
from tickets.views import TicketViewSet
from chats.views import ChatViewSet, RoomView


router = routers.DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'chats', ChatViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterUserAPIView.as_view()),
    path('api/users/<int:pk>/', UserDetailAPI.as_view(), name='user-detail'),
    path('chats/<int:pk>/', RoomView.as_view(), name='chat-room'),
]

urlpatterns += [path("api/auth/", TokenObtainPairView.as_view(),
                     name="jwt_obtain_pair"),
                path("api/auth/refresh/", TokenRefreshView.as_view(),
                     name="jwt_refresh"),
                ]

# development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
