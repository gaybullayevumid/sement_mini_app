from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Product, Order

class SementMarketView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['orders'] = Order.objects.all().order_by('-id')  # Barcha buyurtmalar, sotuvchi interfeysda ko‘rinadi
        return context

class OrderAddView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        client = request.POST.get('client')
        seller = request.POST.get('seller')
        if not (product_id and quantity and client and seller):
            return JsonResponse({"success": False, "error": "Missing data"})

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"})

        try:
            quantity = int(quantity)
        except ValueError:
            return JsonResponse({"success": False, "error": "Invalid quantity"})

        total_price = quantity * product.price

        order = Order.objects.create(
            client=client,
            product=product,
            seller=seller,
            quantity=quantity,
            total_price=total_price,
            status="pending"
        )
        return JsonResponse({"success": True, "order_id": order.id})

class MyPendingOrdersView(View):
    def get(self, request):
        client = request.GET.get("client")
        if not client:
            return JsonResponse({"orders": []})
        orders = Order.objects.filter(client=client, status="pending").order_by('-id')
        data = [
            {
                "id": o.id,
                "name": o.product.name,
                "quantity": o.quantity,
                "price": o.total_price,
                "product_id": o.product.id,
            }
            for o in orders
        ]
        return JsonResponse({"orders": data})

@method_decorator(csrf_exempt, name='dispatch')
class CancelOrderView(View):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            if order.status == "pending":
                order.status = "canceled"
                order.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Buyurtma allaqachon tasdiqlangan yoki bekor qilingan"})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Buyurtma topilmadi"})