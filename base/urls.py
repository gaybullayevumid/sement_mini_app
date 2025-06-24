from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    ProductViewSet,
    OrderViewSet,
    CartViewSet,
    SellerViewSet,
    SellerProductViewSet,
    SellerOrderViewSet,
    ClientViewSet,
)

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"carts", CartViewSet, basename="cart")
router.register(r"sellers", SellerViewSet)
router.register(r"clients", ClientViewSet, basename="client")  # ClientViewSet uchun ro'yxat va actions

sellers_router = routers.NestedDefaultRouter(router, r"sellers", lookup="seller")
sellers_router.register(r"products", SellerProductViewSet, basename="seller-products")
sellers_router.register(r"orders", SellerOrderViewSet, basename="seller-orders")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(sellers_router.urls)),
]