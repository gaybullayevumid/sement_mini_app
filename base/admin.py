from django.contrib import admin
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = [
        "telegram_id",
        "first_name",
        "last_name",
        "username",
        "phone_number",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["first_name", "last_name", "username", "phone_number"]
    readonly_fields = ["telegram_id", "created_at", "updated_at"]

    fieldsets = (
        ("Telegram Ma'lumotlari", {"fields": ("telegram_id", "username")}),
        (
            "Shaxsiy Ma'lumotlar",
            {"fields": ("first_name", "last_name", "phone_number")},
        ),
        ("Holat", {"fields": ("is_active",)}),
        ("Vaqt Ma'lumotlari", {"fields": ("created_at", "updated_at")}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return list(self.readonly_fields) + ['telegram_id']
        return self.readonly_fields
