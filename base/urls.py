from django.urls import path
from .views import HomePageView, ProductPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("products/", ProductPageView.as_view(), name="product"),
]
