# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class TelegramUser(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use telegram_id as the unique identifier for authentication
    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = ['phone_number']  # Minimal talablar

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''} (@{self.username or 'no_username'})"

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"
        ordering = ['-created_at']