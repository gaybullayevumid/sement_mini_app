from django.urls import path
from .views import SementMarketView

urlpatterns = [
    path("", SementMarketView.as_view(), name="home"),
    # path("products/", SementMarketView.as_view(), name="product"),
]
