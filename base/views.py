from django.views.generic import TemplateView
from .models import Product, Order

class SementMarketView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['orders'] = Order.objects.all().order_by('-id')
        return context