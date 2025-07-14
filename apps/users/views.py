from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import UserSerializer
from apps.products.serializers import SellerWithProductsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"])
    def sellers(self, request):
        sellers = CustomUser.objects.filter(user_type="seller")
        serializer = SellerWithProductsSerializer(sellers, many=True)
        return Response(serializer.data)
