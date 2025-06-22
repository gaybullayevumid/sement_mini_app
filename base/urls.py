from django.urls import path
from .views import SementMarketView, OrderAddView, MyPendingOrdersView, CancelOrderView

urlpatterns = [
    path('', SementMarketView.as_view(), name='sement_market'),
    path('order/add/', OrderAddView.as_view(), name='order_add'),
    path('order/my_pending/', MyPendingOrdersView.as_view(), name='my_pending_orders'),
    path('order/cancel/<int:order_id>/', CancelOrderView.as_view(), name='cancel_order'),
]