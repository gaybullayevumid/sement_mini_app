from rest_framework import serializers
from .models import CustomUser, Product, Order, Cart

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'phone', 'user_type']

class ProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'seller']

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