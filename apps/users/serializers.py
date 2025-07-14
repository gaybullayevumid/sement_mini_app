from rest_framework import serializers
from apps.products.serializers import ProductSerializer
from .models import CustomUser

class SellerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']

class UserSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'phone', 'user_type', 'products']

    def get_products(self, obj):
        products = obj.products.all()
        return ProductSerializer(products, many=True).data
