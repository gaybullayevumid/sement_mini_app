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
    

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=100)
    total = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return self.customer