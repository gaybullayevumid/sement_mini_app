from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Brand, Category, Product, Cart, Order, CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "user_type", "is_active", "is_staff")
    list_filter = ("user_type", "is_active", "is_staff")
    
    # fieldsets ni list qilib, yangi fieldlarni qo‘shib, oxirida tuple ga aylantiramiz
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets.append(
        (None, {"fields": ("user_type", "phone")})
    )
    fieldsets = tuple(fieldsets)

    add_fieldsets = list(UserAdmin.add_fieldsets)
    add_fieldsets.append(
        (None, {"fields": ("user_type", "phone")})
    )
    add_fieldsets = tuple(add_fieldsets)

    search_fields = ("username", "email", "phone")
    ordering = ("id",)

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)