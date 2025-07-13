from rest_framework import serializers
from .models import CustomUser
from apps.products.serializers import ProductSerializer

# Simple seller serializer for ProductSerializer
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
