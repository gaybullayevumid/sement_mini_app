from rest_framework import serializers
from .models import CustomUser, Product, Order, Cart, Brand, Category

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'quantity', 'brand', 'seller', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'phone', 'user_type', 'products']

    def get_products(self, obj):
        if obj.user_type == "seller":
            products = obj.products.all()
            return ProductSerializer(products, many=True).data
        return []

# Qolgan serializerlar o'zgarishsiz qoladi
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