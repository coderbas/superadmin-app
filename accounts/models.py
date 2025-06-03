# accounts/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    # Override the default `groups` and `user_permissions` fields so they don't clash with auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='accounts_users',   # a unique reverse name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
        related_query_name='account_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='accounts_users',   # a unique reverse name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='account_user'
    )

    def __str__(self):
        return self.email

# accounts/models.py (continued)

class Page(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='permissions')
    can_view = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'page')

    def __str__(self):
        return f"{self.user.email} – {self.page.name}"
class Comment(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.page.name}] {self.user.email}"

class CommentHistory(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='histories')
    previous_content = models.TextField()
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modifications')
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for comment {self.comment.id} at {self.modified_at}"

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.user.email}"
# accounts/models.py



class Product(models.Model):
    """
    A minimal Product model. Adjust fields as needed.
    """
    name = models.CharField(max_length=200, help_text="Product name")
    description = models.TextField(
        blank=True,
        help_text="Optional longer description of the product",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Unit price in USD (or your currency)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} (${self.price})"
