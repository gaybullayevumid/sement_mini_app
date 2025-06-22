from django.views.generic import TemplateView, ListView
from .models import User, Product, Order

# Create your views here.


class HomePageView(TemplateView):
    template_name = "pages/home.html"

class ProductPageView(ListView):
    model = Product
    template_name = "pages/products.html"
    context_object_name = "products"