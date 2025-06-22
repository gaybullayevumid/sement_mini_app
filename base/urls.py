from django.urls import path
from .views import SementMarketView, OrderAddView

urlpatterns = [
    path('', SementMarketView.as_view(), name='sement_market'),
    path('order/add/', OrderAddView.as_view(), name='order_add'),
]