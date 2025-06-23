from rest_framework import viewsets, permissions
from .models import Product, Cart, Order
from .serializers import ProductSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


# class CartViewSet(viewsets.ModelViewSet):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = [permissions.AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
