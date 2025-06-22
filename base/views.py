from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import Product, Order

class SementMarketView(TemplateView):
    template_name = "sement_market.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['orders'] = Order.objects.all().order_by('-id')
        return context

class OrderAddView(View):
    def post(self, request):
        # AJAX orqali keladigan ma'lumotlar
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        client = request.POST.get('client')
        seller = request.POST.get('seller')
        product = Product.objects.get(id=product_id)
        total_price = int(quantity) * product.price

        order = Order.objects.create(
            client=client,
            product=product,
            seller=seller,
            quantity=quantity,
            total_price=total_price,
            status="pending"
        )
        return JsonResponse({"success": True, "order_id": order.id})