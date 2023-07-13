from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from userauth.views import RegisterUserAPIView, UserDetailAPI


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/register/', RegisterUserAPIView.as_view()),
    path('api/users/<int:pk>/', UserDetailAPI.as_view(), name='user-detail'),
]

urlpatterns += [path("api/auth/", TokenObtainPairView.as_view(),
                     name="jwt_obtain_pair"),
                path("api/auth/refresh/", TokenRefreshView.as_view(),
                     name="jwt_refresh"),
                ]
