from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Product, Cart, Order, Seller
from .serializers import (
    ProductSerializer,
    CartSerializer,
    OrderSerializer,
    SellerSerializer,
    SellerCreateSerializer,
    SellerProductSerializer,
    SellerOrderSerializer,
)


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return SellerCreateSerializer
        return SellerSerializer

    @action(detail=False, methods=["post"])
    def login_or_register(self, request):
        """Telegram orqali login yoki register"""
        telegram_id = request.data.get("telegram_id")
        telegram_username = request.data.get("telegram_username", "")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")

        if not telegram_id:
            return Response(
                {"error": "telegram_id majburiy"}, status=status.HTTP_400_BAD_REQUEST
            )

        seller, created = Seller.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "telegram_username": telegram_username,
                "first_name": first_name,
                "last_name": last_name,
                "business_name": f"{first_name} biznes",
                "phone_number": "",
                "address": "",
            },
        )

        serializer = SellerSerializer(seller)
        return Response(
            {
                "seller": serializer.data,
                "is_new": created,
                "message": "Yangi seller yaratildi" if created else "Seller topildi",
            }
        )

    @action(detail=True, methods=["get"])
    def products(self, request, pk=None):
        """Seller mahsulotlarini olish"""
        seller = self.get_object()
        products = seller.products.all()

        is_available = request.query_params.get("is_available")
        if is_available is not None:
            products = products.filter(is_available=is_available.lower() == "true")

        search = request.query_params.get("search")
        if search:
            products = products.filter(
                Q(name__icontains=search)
                | Q(brand__icontains=search)
                | Q(type__icontains=search)
            )

        serializer = SellerProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_product(self, request, pk=None):
        """Seller mahsulot qo'shishi"""
        seller = self.get_object()
        serializer = SellerProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(seller=seller)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def orders(self, request, pk=None):
        """Seller buyurtmalarini olish"""
        seller = self.get_object()
        orders = seller.orders.all()

        order_status = request.query_params.get("status")
        if order_status:
            orders = orders.filter(status=order_status)

        serializer = SellerOrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def dashboard(self, request, pk=None):
        """Seller dashboard ma'lumotlari"""
        seller = self.get_object()

        total_products = seller.products.count()
        active_products = seller.products.filter(is_available=True).count()
        total_orders = seller.orders.count()
        pending_orders = seller.orders.filter(status="pending").count()
        completed_orders = seller.orders.filter(status="delivered").count()

        recent_orders = seller.orders.all()[:5]
        recent_orders_data = SellerOrderSerializer(recent_orders, many=True).data

        return Response(
            {
                "statistics": {
                    "total_products": total_products,
                    "active_products": active_products,
                    "total_orders": total_orders,
                    "pending_orders": pending_orders,
                    "completed_orders": completed_orders,
                },
                "recent_orders": recent_orders_data,
            }
        )


class SellerProductViewSet(viewsets.ModelViewSet):
    serializer_class = SellerProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        seller_id = self.kwargs.get("seller_pk")
        return Product.objects.filter(seller_id=seller_id)

    def perform_create(self, serializer):
        seller_id = self.kwargs.get("seller_pk")
        seller = get_object_or_404(Seller, pk=seller_id)
        serializer.save(seller=seller)


class SellerOrderViewSet(viewsets.ModelViewSet):
    serializer_class = SellerOrderSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        seller_id = self.kwargs.get("seller_pk")
        return Order.objects.filter(seller_id=seller_id)

    @action(detail=True, methods=["patch"])
    def update_status(self, request, seller_pk=None, pk=None):
        """Buyurtma statusini yangilash"""
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"error": "Noto'g'ri status"}, status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        serializer = SellerOrderSerializer(order)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(brand__icontains=search)
                | Q(type__icontains=search)
            )

        # Filter by seller
        seller_id = self.request.query_params.get("seller")
        if seller_id:
            queryset = queryset.filter(seller_id=seller_id)

        return queryset


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        if user_id:
            return Cart.objects.filter(user_id=user_id)
        return Cart.objects.none()

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        """Mahsulotni savatchaga qo'shish"""
        user_id = request.data.get("user_id")
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if not user_id or not product_id:
            return Response(
                {"error": "user_id va product_id majburiy"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = get_object_or_404(Product, id=product_id, is_available=True)

        cart_item, created = Cart.objects.get_or_create(
            user_id=user_id, product=product, defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart_item)
        return Response(serializer.data)

    @action(detail=False, methods=["delete"])
    def clear_cart(self, request):
        """Savatchani tozalash"""
        user_id = request.query_params.get("user_id")
        if user_id:
            Cart.objects.filter(user_id=user_id).delete()
            return Response({"message": "Savatcha tozalandi"})
        return Response(
            {"error": "user_id majburiy"}, status=status.HTTP_400_BAD_REQUEST
        )


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        client_telegram_id = self.request.query_params.get("client_telegram_id")
        if client_telegram_id:
            return Order.objects.filter(client_telegram_id=client_telegram_id)
        return Order.objects.all()

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        total_price = product.price * quantity

        serializer.save(total_price=total_price, seller=product.seller)
