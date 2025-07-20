from rest_framework import serializers
from apps.users.models import CustomUser
from .models import  Product, Order, Cart, Brand, Category


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'quantity', 'brand', 'seller', 'created_at']

    def get_seller(self, obj):
        from apps.users.serializers import SellerShortSerializer  # 👈 bu yerga ko'chirildi
        return SellerShortSerializer(obj.seller).data

class SellerWithProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'phone', 'user_type', 'products']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'created_at']

class CartSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'client', 'orders']