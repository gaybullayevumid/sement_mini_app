from django.urls import path
from .views import (
    SementMarketView, OrderAddView, MyPendingOrdersView, CancelOrderView,
    AddToCartView, CartView, RemoveFromCartView, UpdateCartView, CheckoutView
)

urlpatterns = [
    path('', SementMarketView.as_view(), name='sement_market'),
    
    # Eski order URL'lari (backward compatibility uchun)
    path('order/add/', OrderAddView.as_view(), name='order_add'),
    path('order/my_pending/', MyPendingOrdersView.as_view(), name='my_pending_orders'),
    path('order/cancel/<int:order_id>/', CancelOrderView.as_view(), name='cancel_order'),
    
    # YANGI: Cart URL'lari
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/view/', CartView.as_view(), name='view_cart'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/update/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/checkout/', CheckoutView.as_view(), name='checkout'),
]