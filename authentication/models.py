import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class OnlineStatus(models.TextChoices):
    ONLINE = "Online", "Online"
    OFFLINE = "Offline", "Offline"


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_verification_otp = models.CharField(max_length=6, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)
    online_status = models.CharField(
        max_length=10,
        choices=OnlineStatus.choices,
        default=OnlineStatus.OFFLINE,
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
