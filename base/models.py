from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("client", "Client"),
        ("seller", "Seller"),
    )
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="client"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
