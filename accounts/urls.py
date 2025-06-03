# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserViewSet,
    PermissionViewSet,
    CommentViewSet,
    PageListView,  ProductViewSet,  
    PasswordResetRequestView,
    PasswordResetVerifyView,
)
# We already registered “token/” in backend/urls.py, so no need to do it here.
from .serializers import MyTokenObtainPairView  # only imported if you ever wanted a second token endpoint here

router = DefaultRouter()
# ───────────────────┐
#  1) Register ViewSets for DRF router:
#     Users  →  /api/users/
#     Permissions → /api/permissions/
#     Comments → /api/comments/
#     (Optionally, Products → /api/products/ if you create a ProductViewSet)
router.register(r"users",       UserViewSet,       basename="user")
router.register(r"permissions", PermissionViewSet, basename="permission")
#router.register(r"products", ProductViewSet, basename="product")
router.register(r"comments",    CommentViewSet,    basename="comment")
# If you have a ProductViewSet, you can also do:
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    # 1) All router‐generated endpoints: /api/users/, /api/permissions/, /api/comments/, (maybe /api/products/)
    path("", include(router.urls)),

    # 2) Read-only list of pages: → GET /api/pages/
    path("pages/", PageListView.as_view(), name="page-list"),

    # 3) Comment history (superuser only): → GET /api/comment-history/

    # 4) Password reset endpoints (optional):
    path("password-reset/request/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/verify/",  PasswordResetVerifyView.as_view(),  name="password_reset_verify"),

    # 5) (Optional) If you still want an extra token endpoint here, you could add:
    #    path("token/",       MyTokenObtainPairView.as_view(),  name="token_obtain_pair"),
    #    path("token/refresh/", TokenRefreshView.as_view(),      name="token_refresh"),
    #
    #    But remember: **only one** location for “token/” and “token/refresh/” is needed.
]
