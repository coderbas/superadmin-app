# accounts/views.py

from rest_framework import generics, status, viewsets, permissions   # <-- Add viewsets & permissions here
from rest_framework.response import Response

# Import your serializers:
from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    UserSerializer,
    UserCreateSerializer,
    PermissionSerializer,
    PageSerializer,
    CommentSerializer,
    CommentHistorySerializer,
    ProductSerializer     # <-- Import ProductSerializer
)

# Import your models:
from .models import (
    Product,    # <-- Import Product model
    User,
    Permission,
    Page,
    Comment,
    CommentHistory
)

# ─── 1) PRODUCT VIEWSET ────────────────────────────────────────────────────────
class ProductViewSet(viewsets.ModelViewSet):
    """
    All authenticated users can see the product list. Adjust permissions as needed.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


# ─── 2) PASSWORD RESET VIEWS ───────────────────────────────────────────────────
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "OTP sent to your email."}, status=status.HTTP_200_OK)


class PasswordResetVerifyView(generics.GenericAPIView):
    serializer_class = PasswordResetVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)


# ─── 3) USER VIEWSET ───────────────────────────────────────────────────────────
class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperuser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer


# ─── 4) PERMISSION VIEWSET ─────────────────────────────────────────────────────
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperuser]

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        serializer.save(user_id=user_id)


# ─── 5) PAGE LIST VIEW ─────────────────────────────────────────────────────────
class PageListView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticated]


# ─── 6) COMMENT VIEWSET ────────────────────────────────────────────────────────
from rest_framework import mixins

class CommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        page_id = self.request.query_params.get("page_id")
        if not page_id:
            return Comment.objects.none()
        return Comment.objects.filter(page_id=page_id).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─── 7) COMMENT HISTORY VIEW ───────────────────────────────────────────────────
class CommentHistoryListView(generics.ListAPIView):
    queryset = CommentHistory.objects.all().order_by('-modified_at')
    serializer_class = CommentHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperuser]
