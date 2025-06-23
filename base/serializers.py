from rest_framework import serializers
from .models import Product, Cart, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


# class CartSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(read_only=True)
#     product_id = serializers.PrimaryKeyRelatedField(
#         queryset=Product.objects.all(), source='product', write_only=True
#     )

#     class Meta:
#         model = Cart
#         fields = ['id', 'user_id', 'product', 'product_id', 'quantity', 'created_at', 'total_price']
#         read_only_fields = ['id', 'created_at', 'total_price']

#     total_price = serializers.SerializerMethodField()

#     def get_total_price(self, obj):
#         return obj.total_price()


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "date",
            "client",
            "seller",
            "product",
            "product_id",
            "quantity",
            "total_price",
            "status",
        ]
        read_only_fields = ["id", "date", "total_price"]
