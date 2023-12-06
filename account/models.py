import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

from django.db import models


class CustomUser(AbstractBaseUser, PermissionsMixin):
    REGD_AS_CHOICES = (
        ("TCH", "TEACHER"),
        ("STU", "STUDENT"),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    email = models.EmailField(unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    last_logged_out = models.DateTimeField(null=True, blank=True)


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"

    objects = CustomUserManager()