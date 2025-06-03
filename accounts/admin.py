from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Page, Permission, Comment, CommentHistory

# 1) Register your custom User model so “Users” shows up in admin.
#    We subclass DjangoUserAdmin so you keep the standard “add/change user” forms.

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # Display these fields in the user list
    list_display = ("email", "username", "is_active", "is_staff", "is_superuser")
    # Filter sidebar
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    # When you click to edit a user, show these sections:
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    # Add‐user form: what fields appear when you click “Add user”
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )
    search_fields = ("email", "username")
    ordering = ("email",)


# 2) Register Page, Permission, Comment, and CommentHistory if you want to manage them in admin too:

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("user", "page", "can_view", "can_create", "can_edit", "can_delete")
    list_filter = ("page", "can_view", "can_create", "can_edit", "can_delete")
    search_fields = ("user__email", "page__name")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "page", "user", "created_at", "updated_at")
    list_filter = ("page", "user")
    search_fields = ("content", "user__email")


@admin.register(CommentHistory)
class CommentHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "modified_by", "modified_at")
    list_filter = ("modified_by",)
    search_fields = ("previous_content", "modified_by__email")

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('created_at',)