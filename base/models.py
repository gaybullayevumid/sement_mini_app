from django.db import models

# Create your models here.


class Seller(models.Model):
    brand = models.CharField(max_length=255)
    type = models.CharField(max_length=200)
    quality = models.IntegerField()
    weight_per_bag = models.IntegerField()
    origin = models.CharField(max_length=200)
    cement_class = models.CharField(max_length=20)

    def __str__(self):
        return self.brand
