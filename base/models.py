from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    quality = models.CharField(max_length=100)
    weight = models.FloatField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True)
    origin = models.CharField(max_length=100)
    cement_class = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

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
        unique_together = ('user_id', 'product')

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    client = models.CharField(max_length=100)
    seller = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"{self.client} - {self.product.name} ({self.quantity}t)"