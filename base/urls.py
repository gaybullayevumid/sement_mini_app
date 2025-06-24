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
)

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"carts", CartViewSet, basename="cart")
router.register(r"sellers", SellerViewSet)

sellers_router = routers.NestedDefaultRouter(router, r"sellers", lookup="seller")
sellers_router.register(r"products", SellerProductViewSet, basename="seller-products")
sellers_router.register(r"orders", SellerOrderViewSet, basename="seller-orders")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(sellers_router.urls)),
]

# API endpoints:
# GET/POST /api/sellers/ - Sellerlar ro'yxati/yaratish
# POST /api/sellers/login_or_register/ - Telegram orqali login/register
# GET /api/sellers/{id}/ - Seller ma'lumotlari
# GET /api/sellers/{id}/products/ - Seller mahsulotlari
# POST /api/sellers/{id}/add_product/ - Seller mahsulot qo'shish
# GET /api/sellers/{id}/orders/ - Seller buyurtmalari
# GET /api/sellers/{id}/dashboard/ - Seller dashboard

# Nested routes:
# GET/POST /api/sellers/{seller_id}/products/ - Seller mahsulotlarini boshqarish
# GET/PUT/PATCH/DELETE /api/sellers/{seller_id}/products/{id}/ - Bitta mahsulot
# GET /api/sellers/{seller_id}/orders/ - Seller buyurtmalari
# PATCH /api/sellers/{seller_id}/orders/{id}/update_status/ - Buyurtma statusini yangilash
