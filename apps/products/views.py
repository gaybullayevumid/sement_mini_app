from rest_framework import viewsets, permissions
from .models import Product, Order, Cart, Brand, Category
from apps.users.models import CustomUser
from .serializers import (
    ProductSerializer,
    OrderSerializer,
    CartSerializer,
    CategorySerializer,
    BrandSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=["get"])
    def products(self, request):
        category_id = request.query_params.get("category_id")
        if category_id:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def my_products(self, request):
        """
        Foydalanuvchi (seller) o'zining barcha productlarini ko'radi
        """
        products = Product.objects.filter(seller=request.user)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer