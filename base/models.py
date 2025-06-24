from django.db import models
from django.contrib.auth.models import User


class Seller(models.Model):
    telegram_id = models.CharField(max_length=100, unique=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business_name} - {self.telegram_username}"

    class Meta:
        db_table = "sellers"


class Product(models.Model):
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    quality = models.CharField(max_length=100)
    weight = models.FloatField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    description = models.TextField(blank=True)
    origin = models.CharField(max_length=100)
    cement_class = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.seller.business_name}"

    class Meta:
        db_table = "products"


class Cart(models.Model):
    user_id = models.CharField(max_length=100)  # Telegram user ID yoki session
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.product.name} ({self.quantity})"

    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ("user_id", "product")
        db_table = "carts"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Kutilmoqda"),
        ("confirmed", "Tasdiqlangan"),
        ("processing", "Tayyorlanmoqda"),
        ("shipped", "Yetkazilmoqda"),
        ("delivered", "Yetkazilgan"),
        ("cancelled", "Bekor qilingan"),
    ]

    date = models.DateTimeField(auto_now_add=True)
    client = models.CharField(max_length=100)
    client_telegram_id = models.CharField(max_length=100)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders"
    )
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    client_address = models.TextField(blank=True, null=True)
    client_phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.client} - {self.product.name} ({self.quantity}t)"

    class Meta:
        db_table = "orders"
        ordering = ["-date"]
