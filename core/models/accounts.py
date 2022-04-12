import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from utils.enums import UserType


class User(AbstractUser):
    """
    USER MODELS
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.PositiveSmallIntegerField(default=0, choices=UserType.choices())
    master = models.ForeignKey('User', on_delete=models.CASCADE, related_name='master_name', null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    newsletter = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False, blank=True)
    first_login = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'
        ordering = ('-created_at',)

    def __str__(self):
        return self.email


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    motto = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class AuthToken(models.Model):
    """
    AUTH TOKEN
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_token_value')
    type_choices = (
        (0, "Reset Token"),
        (1, "Login Token"),
        (2, "Email Confirmation"),
        (3, "Authorization Token"),
        (4, "User invitation Token"),
    )
    type = models.PositiveSmallIntegerField(choices=type_choices, default=0)
    token = models.CharField(max_length=255, null=True, blank=True, editable=False)
    status = models.BooleanField(default=False)
    expiry = models.DateTimeField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} {1}".format(str(self.user), str(self.created_at))

    class Meta:
        ordering = ("-created_at",)
        db_table = "user_token"
        verbose_name = "Token"
