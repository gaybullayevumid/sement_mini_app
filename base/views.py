from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from .models import Product, Cart, Order, Seller, Client, OrderNotification
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    ProductSerializer,
    CartSerializer,
    OrderSerializer,
    SellerSerializer,
    SellerCreateSerializer,
    SellerProductSerializer,
    SellerOrderSerializer,
    ClientSerializer,
    OrderCreateSerializer,
    OrderNotificationSerializer,
)

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return SellerCreateSerializer
        return SellerSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['telegram_id'],
            properties={
                'telegram_id': openapi.Schema(type=openapi.TYPE_STRING, description='Telegram ID'),
                'telegram_username': openapi.Schema(type=openapi.TYPE_STRING, description='Telegram username'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
            },
        )
    )
    @action(detail=False, methods=["post"])
    def login_or_register(self, request):
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
        seller = self.get_object()
        products = seller.products.all()
        is_available = request.query_params.get("is_available")
        if is_available is not None:
            products = products.filter(is_available=is_available.lower() == "true")
        search = request.query_params.get("search")
        if search:
            products = products.filter(
                Q(name__icontains=search) | Q(brand__icontains=search) | Q(type__icontains=search)
            )
        serializer = SellerProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_product(self, request, pk=None):
        seller = self.get_object()
        serializer = SellerProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=seller)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def orders(self, request, pk=None):
        seller = self.get_object()
        orders = seller.orders.all()
        order_status = request.query_params.get("status")
        if order_status:
            orders = orders.filter(status=order_status)
        serializer = SellerOrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def dashboard(self, request, pk=None):
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

class ClientAuthView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['telegram_id'],
            properties={
                'telegram_id': openapi.Schema(type=openapi.TYPE_STRING, description='Telegram ID'),
                'telegram_username': openapi.Schema(type=openapi.TYPE_STRING, description='Telegram username'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
            },
        )
    )
    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        telegram_username = request.data.get("telegram_username", "")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        if not telegram_id:
            return Response(
                {"error": "telegram_id majburiy"}, status=status.HTTP_400_BAD_REQUEST
            )
        client, created = Client.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "telegram_username": telegram_username,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": "",
                "address": "",
            },
        )
        serializer = ClientSerializer(client)
        return Response(
            {
                "client": serializer.data,
                "is_new": created,
                "message": "Yangi client yaratildi" if created else "Client topildi",
            }
        )

    def get(self, request):
        """
        Get client by telegram_id (pass as query param).
        """
        telegram_id = request.query_params.get("telegram_id")
        if not telegram_id:
            return Response(
                {"error": "telegram_id majburiy"}, status=status.HTTP_400_BAD_REQUEST
            )
        client = get_object_or_404(Client, telegram_id=telegram_id)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request):
        """
        Update (replace) client info by telegram_id (pass as data param).
        """
        telegram_id = request.data.get("telegram_id")
        if not telegram_id:
            return Response(
                {"error": "telegram_id majburiy"}, status=status.HTTP_400_BAD_REQUEST
            )
        client = get_object_or_404(Client, telegram_id=telegram_id)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        Partial update client info by telegram_id (pass as data param).
        """
        telegram_id = request.data.get("telegram_id")
        if not telegram_id:
            return Response(
                {"error": "telegram_id majburiy"}, status=status.HTTP_400_BAD_REQUEST
            )
        client = get_object_or_404(Client, telegram_id=telegram_id)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SellerOrderViewSet(viewsets.ModelViewSet):
    serializer_class = SellerOrderSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        seller_id = self.kwargs.get("seller_pk")
        return Order.objects.filter(seller_id=seller_id)

    @action(detail=True, methods=["patch"])
    def update_status(self, request, seller_pk=None, pk=None):
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
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(brand__icontains=search) | Q(type__icontains=search)
            )
        seller_id = self.request.query_params.get("seller")
        if seller_id:
            queryset = queryset.filter(seller_id=seller_id)
        return queryset

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        client_id = self.request.query_params.get("client_id")
        if client_id:
            return Cart.objects.filter(client_id=client_id)
        return Cart.objects.none()

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        client_id = request.data.get("client_id")
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        if not client_id or not product_id:
            return Response(
                {"error": "client_id va product_id majburiy"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        product = get_object_or_404(Product, id=product_id, is_available=True)
        cart_item, created = Cart.objects.get_or_create(
            client_id=client_id, product=product, defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        serializer = CartSerializer(cart_item)
        return Response(serializer.data)

    @action(detail=False, methods=["delete"])
    def clear_cart(self, request):
        client_id = request.query_params.get("client_id")
        if client_id:
            Cart.objects.filter(client_id=client_id).delete()
            return Response({"message": "Savatcha tozalandi"})
        return Response(
            {"error": "client_id majburiy"}, status=status.HTTP_400_BAD_REQUEST
        )

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        client_id = self.request.query_params.get("client_id")
        if client_id:
            return Order.objects.filter(client_id=client_id)
        return Order.objects.all()

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        total_price = product.price * quantity
        serializer.save(total_price=total_price, seller=product.seller)