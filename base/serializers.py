from rest_framework import serializers
from .models import Product, Cart, Order, Seller, Client, OrderNotification

class SellerSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model = Seller
        fields = [
            "id", "telegram_id", "telegram_username", "first_name", "last_name",
            "business_name", "phone_number", "address", "is_active",
            "created_at", "updated_at", "products_count",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "products_count"]

    def get_products_count(self, obj):
        return obj.products.filter(is_available=True).count()

class SellerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = [
            "telegram_id", "telegram_username", "first_name", "last_name",
            "business_name", "phone_number", "address",
        ]

class ClientSerializer(serializers.ModelSerializer):
    orders_count = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = [
            "id", "telegram_id", "telegram_username", "first_name", "last_name",
            "phone_number", "address", "is_active", "orders_count", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "is_active", "orders_count"]

    def get_orders_count(self, obj):
        return obj.orders.count()

class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source="seller.business_name", read_only=True)
    class Meta:
        model = Product
        fields = [
            "id", "seller", "seller_name", "name", "brand", "type", "quality",
            "weight", "image", "description", "origin", "cement_class", "price",
            "is_available", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "seller_name"]

class SellerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id", "name", "brand", "type", "quality", "weight", "image", "description",
            "origin", "cement_class", "price", "is_available", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )
    total_price = serializers.SerializerMethodField()
    seller_name = serializers.CharField(source="product.seller.business_name", read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id", "client", "product", "product_id", "quantity", "total_price",
            "seller_name", "created_at",
        ]
        read_only_fields = ["id", "created_at", "total_price", "seller_name"]

    def get_total_price(self, obj):
        return obj.total_price()

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )
    seller_name = serializers.CharField(source="seller.business_name", read_only=True)
    client_name = serializers.CharField(source="client.first_name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "date", "client", "client_name", "seller", "seller_name",
            "product", "product_id", "quantity", "total_price", "status", "status_display",
            "client_address", "client_phone", "notes", "delivery_date",
        ]
        read_only_fields = [
            "id", "order_number", "date", "total_price", "seller_name", "client_name", "status_display"
        ]

class SellerOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.ImageField(source="product.image", read_only=True)
    client_name = serializers.CharField(source="client.first_name", read_only=True)
    client_username = serializers.CharField(source="client.telegram_username", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "date", "client_name", "client_username", "product_name",
            "product_image", "quantity", "total_price", "status", "status_display",
            "client_address", "client_phone", "notes", "delivery_date",
        ]
        read_only_fields = [
            "id", "order_number", "date", "total_price", "product_name",
            "product_image", "client_name", "client_username", "status_display"
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()), write_only=True
    )
    class Meta:
        model = Order
        fields = [
            "client", "client_address", "client_phone", "notes", "items"
        ]

    def create(self, validated_data):
        items = validated_data.pop('items')
        client = validated_data['client']
        orders = []
        for item in items:
            product = Product.objects.get(id=item['product_id'])
            quantity = int(item['quantity'])
            order = Order.objects.create(
                client=client,
                seller=product.seller,
                product=product,
                quantity=quantity,
                total_price=product.price * quantity,
                client_address=validated_data.get('client_address', ''),
                client_phone=validated_data.get('client_phone', ''),
                notes=validated_data.get('notes', '')
            )
            orders.append(order)
            # Notification
            OrderNotification.objects.create(
                order=order,
                recipient_type='seller',
                recipient_telegram_id=product.seller.telegram_id,
                notification_type='new_order',
                message=f"Yangi buyurtma: {product.name} - {quantity} dona"
            )
        return orders[0] if orders else None

class OrderNotificationSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source="order.order_number", read_only=True)
    class Meta:
        model = OrderNotification
        fields = [
            "id", "order", "order_number", "notification_type", "message",
            "is_read", "created_at"
        ]
        read_only_fields = ["id", "created_at", "order_number"]