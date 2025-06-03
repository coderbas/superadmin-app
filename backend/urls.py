# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from accounts.serializers import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # 1) Django admin:
    path("admin/", admin.site.urls),

    # 2) Custom JWT “obtain pair” endpoint:
    #    → POST http://127.0.0.1:8000/api/token/   (body: { "username": "...", "password": "..." })
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),

    # 3) JWT “refresh” (built-in):
    #    → POST http://127.0.0.1:8000/api/token/refresh/  (body: { "refresh": "<refresh_token>" })
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 4) All other “/api/…” endpoints are delegated to accounts/urls.py
    #    This is where our router will register users, permissions, comments, etc.
    path("api/", include("accounts.urls")),
]
