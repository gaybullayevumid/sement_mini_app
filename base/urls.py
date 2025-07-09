from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    ProductViewSet,
    CartViewSet,
    OrderViewSet,
    BrandViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"products", ProductViewSet)
router.register(r"carts", CartViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"brands", BrandViewSet)
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
]
