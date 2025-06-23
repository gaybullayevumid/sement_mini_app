from django.contrib import admin
from .models import Product, Order, Cart


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "brand", "type", "price", "weight"]
    list_filter = ["brand", "type", "cement_class"]
    search_fields = ["name", "brand"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user_id", "product", "quantity", "total_price", "created_at"]
    list_filter = ["created_at", "product"]
    search_fields = ["user_id", "product__name"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "client",
        "product",
        "quantity",
        "total_price",
        "status",
        "date",
    ]
    list_filter = ["status", "date", "product"]
    search_fields = ["client", "product__name"]
