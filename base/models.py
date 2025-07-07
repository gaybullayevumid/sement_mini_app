from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        ('client', 'Client'),
        ('seller', 'Seller'),
    )
    telegram_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='client')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_user_type_display()})"  # type: ignore
    class Meta:
        db_table = 'custom_user'