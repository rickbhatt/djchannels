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
            None,
            {
                "fields": (
                    "id",
                    "email",
                    "last_login",
                    "last_logged_out",
                    "password",
                ),
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
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = (
        "id",
        "email",
    )
