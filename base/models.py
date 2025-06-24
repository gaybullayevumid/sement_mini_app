from django.db import models

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

class Client(models.Model):
    telegram_id = models.CharField(max_length=100, unique=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.telegram_username}"

    class Meta:
        db_table = "clients"

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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.first_name} - {self.product.name} ({self.quantity})"

    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ("client", "product")
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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    client_address = models.TextField(blank=True, null=True)
    client_phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    order_number = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.client.first_name} - {self.product.name}"

    class Meta:
        db_table = "orders"
        ordering = ["-date"]

class OrderNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_order', 'Yangi buyurtma'),
        ('status_changed', 'Status o\'zgarishi'),
        ('order_cancelled', 'Buyurtma bekor qilindi'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="notifications")
    recipient_type = models.CharField(max_length=10, choices=[('client', 'Client'), ('seller', 'Seller')])
    recipient_telegram_id = models.CharField(max_length=100)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order_notifications"
        ordering = ["-created_at"]