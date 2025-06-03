from rest_framework import serializers
from .models import User, Permission, Page, Comment, CommentHistory
from django.contrib.auth.password_validation import validate_password

# accounts/serializers.py


from .models import Product   # ← Make sure you have a Product model!

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            # … add any other fields your Product model has …
        ]

# accounts/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["is_superuser"] = user.is_superuser
        # (Optionally add any other fields you need here)
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'is_superuser']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.is_superuser = validated_data.get('is_superuser', False)
        user.is_active = True
        user.save()
        return user
class UserCreateSerializer(serializers.ModelSerializer):
    """
    Used for creating a new user. Exposes: username, email, password.
    The create() method calls create_user(...) so that password is hashed.
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # We allow the front end to supply username, email, and password.
        # We do NOT allow the front end to set is_staff or is_superuser directly here.
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """
        Create a new user with a hashed password.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'name')

class PermissionSerializer(serializers.ModelSerializer):
    page = PageSerializer(read_only=True)
    page_id = serializers.PrimaryKeyRelatedField(
        queryset=Page.objects.all(), source='page', write_only=True
    )

    class Meta:
        model = Permission
        fields = ('id', 'user', 'page', 'page_id', 'can_view', 'can_create', 'can_edit', 'can_delete')
        read_only_fields = ('id', 'user', 'page')

class CommentHistorySerializer(serializers.ModelSerializer):
    modified_by = UserSerializer(read_only=True)

    class Meta:
        model = CommentHistory
        fields = ('id', 'previous_content', 'modified_by', 'modified_at')

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    histories = CommentHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'page', 'user', 'content', 'created_at', 'updated_at', 'histories')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'histories')

# accounts/serializers.py (continued)

import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        otp = random.randint(100000, 999999)

        # store OTP & expiry in a simple model or cache
        # For simplicity, use a one‐time model:

        from .models import PasswordResetOTP
        otp_entry = PasswordResetOTP.objects.create(user=user, otp=otp,
                           expires_at=timezone.now() + timedelta(minutes=15))
        # Send email – configure your EMAIL_* settings in settings.py
        send_mail(
            subject="Your password reset OTP",
            message=f"Your OTP is {otp}. It expires in 15 minutes.",
            from_email="no‐reply@yourdomain.com",
            recipient_list=[email]
        )
        return otp_entry

class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or OTP.")
        from .models import PasswordResetOTP
        try:
            otp_entry = PasswordResetOTP.objects.get(user=user, otp=otp)
        except PasswordResetOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP.")
        if otp_entry.expires_at < timezone.now():
            raise serializers.ValidationError("OTP has expired.")
        attrs['user'] = user
        attrs['otp_entry'] = otp_entry
        return attrs

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        validate_password(new_password)  # run Django’s password validators
        user.set_password(new_password)
        user.save()
        # Delete OTP entry
        self.validated_data['otp_entry'].delete()
        return user
