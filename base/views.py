from rest_framework import viewsets, permissions
from .models import CustomUser, Product, Order, Cart
from .serializers import UserSerializer, ProductSerializer, OrderSerializer, CartSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def sellers(self, request):
        sellers = CustomUser.objects.filter(user_type='seller')
        serializer = self.get_serializer(sellers, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer