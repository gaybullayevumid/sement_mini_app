from django.contrib import admin
from .models import Seller, Product, Order

# Register your models here.

admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Order)
