from django.contrib import admin
from .models import Product, Order, Cart, Seller

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = [
        "business_name",
        "telegram_username",
        "first_name",
        "last_name",
        "phone_number",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["business_name", "telegram_username", "first_name", "telegram_id"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Telegram Ma'lumotlar",
            {"fields": ("telegram_id", "telegram_username", "first_name", "last_name")},
        ),
        (
            "Biznes Ma'lumotlar",
            {"fields": ("business_name", "phone_number", "address")},
        ),
        ("Status", {"fields": ("is_active",)}),
        ("Vaqtlar", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "seller",
        "brand",
        "type",
        "price",
        "weight",
        "is_available",
        "created_at",
    ]
    list_filter = [
        "seller",
        "brand",
        "type",
        "cement_class",
        "is_available",
        "created_at",
    ]
    search_fields = ["name", "brand", "seller__business_name"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Asosiy Ma'lumotlar",
            {"fields": ("seller", "name", "brand", "type", "quality")},
        ),
        (
            "Texnik Ma'lumotlar",
            {"fields": ("weight", "origin", "cement_class", "price")},
        ),
        ("Qo'shimcha", {"fields": ("description", "image", "is_available")}),
        ("Vaqtlar", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["client", "product", "quantity", "total_price", "created_at"]
    list_filter = ["created_at", "product__seller"]
    search_fields = ["client__first_name", "product__name"]

    def total_price(self, obj):
        return obj.total_price()

    total_price.short_description = "Jami narx"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "client",
        "seller",
        "product",
        "quantity",
        "total_price",
        "status",
        "date",
    ]
    list_filter = ["status", "date", "seller", "product__type"]
    search_fields = [
        "client__first_name",
        "product__name",
        "seller__business_name",
    ]
    readonly_fields = ["date"]

    fieldsets = (
        (
            "Buyurtma Ma'lumotlar",
            {"fields": ("client", "seller", "product")},
        ),
        ("Miqdor va Narx", {"fields": ("quantity", "total_price", "status")}),
        ("Mijoz Ma'lumotlar", {"fields": ("client_address", "client_phone", "notes")}),
        ("Vaqt", {"fields": ("date",)}),
    )

    actions = ["mark_as_confirmed", "mark_as_delivered", "mark_as_cancelled"]

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status="confirmed")
        self.message_user(request, f"{queryset.count()} ta buyurtma tasdiqlandi.")

    mark_as_confirmed.short_description = "Tanlangan buyurtmalarni tasdiqlash"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status="delivered")
        self.message_user(
            request, f"{queryset.count()} ta buyurtma yetkazildi deb belgilandi."
        )

    mark_as_delivered.short_description = (
        "Tanlangan buyurtmalarni yetkazilgan deb belgilash"
    )

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="cancelled")
        self.message_user(request, f"{queryset.count()} ta buyurtma bekor qilindi.")

    mark_as_cancelled.short_description = "Tanlangan buyurtmalarni bekor qilish"