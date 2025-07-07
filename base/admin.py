from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'user_type', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_active', 'created_at')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'telegram_id')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Telegram info', {
            'fields': ('telegram_id', 'user_type')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'user_type'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

    @admin.action(description="Tanlangan foydalanuvchilarni Sotuvchi qilish")
    def make_seller(self, request, queryset):
        updated = queryset.update(user_type='seller')
        self.message_user(request, f'{updated} ta foydalanuvchi Sotuvchi qilindi.')

    @admin.action(description="Tanlangan foydalanuvchilarni Mijoz qilish")
    def make_client(self, request, queryset):
        updated = queryset.update(user_type='client')
        self.message_user(request, f'{updated} ta foydalanuvchi Mijoz qilindi.')

    actions = ['make_seller', 'make_client']