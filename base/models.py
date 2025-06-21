from django.db import models

# Create your models here.

ROLE_CHOICES = [
    ("client", "Client"),
    ("seller", "Seller"),
]


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=200)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=255)
    type = models.CharField(max_length=200)
    quality = models.IntegerField()
    weight = models.IntegerField()
    image = models.ImageField(upload_to="cement-image/")
    description = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    cement_class = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.CharField(max_length=255)
    quantity = models.CharField(max_length=200)
    total_price = models.IntegerField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client


class Seller(models.Model):
    pass
