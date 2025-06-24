from rest_framework import serializers
from .models import Product, Cart, Order, Seller


class SellerSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = [
            "id",
            "telegram_id",
            "telegram_username",
            "first_name",
            "last_name",
            "business_name",
            "phone_number",
            "address",
            "is_active",
            "created_at",
            "updated_at",
            "products_count",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "products_count"]

    def get_products_count(self, obj):
        return obj.products.filter(is_available=True).count()


class SellerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = [
            "telegram_id",
            "telegram_username",
            "first_name",
            "last_name",
            "business_name",
            "phone_number",
            "address",
        ]


class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source="seller.business_name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "seller_name",
            "name",
            "brand",
            "type",
            "quality",
            "weight",
            "image",
            "description",
            "origin",
            "cement_class",
            "price",
            "is_available",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "seller_name"]


class SellerProductSerializer(serializers.ModelSerializer):
    """Seller o'z mahsulotlarini boshqarish uchun"""

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "type",
            "quality",
            "weight",
            "image",
            "description",
            "origin",
            "cement_class",
            "price",
            "is_available",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )
    seller_name = serializers.CharField(source="seller.business_name", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "date",
            "client",
            "client_telegram_id",
            "seller",
            "seller_name",
            "product",
            "product_id",
            "quantity",
            "total_price",
            "status",
            "client_address",
            "client_phone",
            "notes",
        ]
        read_only_fields = ["id", "date", "total_price", "seller_name"]


class SellerOrderSerializer(serializers.ModelSerializer):
    """Seller o'z buyurtmalarini ko'rish uchun"""

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "date",
            "client",
            "client_telegram_id",
            "product_name",
            "product_image",
            "quantity",
            "total_price",
            "status",
            "client_address",
            "client_phone",
            "notes",
        ]
        read_only_fields = [
            "id",
            "date",
            "total_price",
            "product_name",
            "product_image",
        ]


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user_id",
            "product",
            "product_id",
            "quantity",
            "created_at",
            "total_price",
        ]
        read_only_fields = ["id", "created_at", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price()
