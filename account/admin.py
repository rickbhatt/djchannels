from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "is_active", "date_joined")
    readonly_fields = ("id",)
    list_filter = ("email",)
    ordering = ("email",)
    fieldsets = (
        (
            "ID",
            {
                "fields": ("id",),
            },
        ),
        (
            "Credentials",
            {
                "fields": (
                    "email",
                    "last_login",
                    "last_logged_out",
                    "password",
                ),
            },
        ),
        (
            "Personal Information",
            {
                "fields": ("user_name",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "Credentials",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
            "Personal Information",
            {
                "classes": ("wide",),
                "fields": ("user_name",),
            },
        ),
    )

    search_fields = (
        "id",
        "email",
    )
