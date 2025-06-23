from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import Product, Order, Cart
import json

class SementMarketView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['orders'] = Order.objects.all().order_by('-id')
        return context

# YANGI: Savatga qo'shish view
@method_decorator(csrf_exempt, name='dispatch')
class AddToCartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            product_id = data.get('product_id')
            user_id = data.get('user_id', 'default_user')  # Telegram user ID
            quantity = int(data.get('quantity', 1))
            
            if not product_id:
                return JsonResponse({"success": False, "error": "Product ID kerak"})
            
            product = get_object_or_404(Product, id=product_id)
            
            # Cart itemni olish yoki yaratish
            cart_item, created = Cart.objects.get_or_create(
                user_id=user_id,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # Agar mavjud bo'lsa, quantity ni oshirish
                cart_item.quantity += quantity
                cart_item.save()
            
            return JsonResponse({
                "success": True, 
                "message": "Savatga qo'shildi",
                "cart_count": Cart.objects.filter(user_id=user_id).count()
            })
            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

# YANGI: Savatni ko'rish
class CartView(View):
    def get(self, request):
        user_id = request.GET.get('user_id', 'default_user')
        cart_items = Cart.objects.filter(user_id=user_id).select_related('product')
        
        data = []
        total = 0
        for item in cart_items:
            item_data = {
                "id": item.id,
                "product_id": item.product.id,
                "product_name": item.product.name,
                "price": item.product.price,
                "quantity": item.quantity,
                "total_price": item.total_price()
            }
            data.append(item_data)
            total += item.total_price()
        
        return JsonResponse({
            "success": True,
            "cart_items": data,
            "total": total,
            "count": len(data)
        })

# YANGI: Savatdan o'chirish
@method_decorator(csrf_exempt, name='dispatch')
class RemoveFromCartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            cart_item_id = data.get('cart_item_id')
            user_id = data.get('user_id', 'default_user')
            
            cart_item = get_object_or_404(Cart, id=cart_item_id, user_id=user_id)
            cart_item.delete()
            
            return JsonResponse({
                "success": True, 
                "message": "Savatdan o'chirildi",
                "cart_count": Cart.objects.filter(user_id=user_id).count()
            })
            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

# YANGI: Savat quantity ni o'zgartirish
@method_decorator(csrf_exempt, name='dispatch')
class UpdateCartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            cart_item_id = data.get('cart_item_id')
            quantity = int(data.get('quantity', 1))
            user_id = data.get('user_id', 'default_user')
            
            if quantity <= 0:
                return JsonResponse({"success": False, "error": "Quantity 0 dan katta bo'lishi kerak"})
            
            cart_item = get_object_or_404(Cart, id=cart_item_id, user_id=user_id)
            cart_item.quantity = quantity
            cart_item.save()
            
            return JsonResponse({
                "success": True, 
                "message": "Quantity o'zgartirildi",
                "new_total": cart_item.total_price()
            })
            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

# YANGI: Checkout - savatdan orderga o'tkazish
@method_decorator(csrf_exempt, name='dispatch')
class CheckoutView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            user_id = data.get('user_id', 'default_user')
            client = data.get('client', 'Mijoz')
            seller = data.get('seller', 'Sotuvchi')
            
            cart_items = Cart.objects.filter(user_id=user_id).select_related('product')
            
            if not cart_items.exists():
                return JsonResponse({"success": False, "error": "Savat bo'sh"})
            
            # Har bir cart item uchun order yaratish
            orders = []
            for item in cart_items:
                order = Order.objects.create(
                    client=client,
                    seller=seller,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.total_price(),
                    status="pending"
                )
                orders.append(order.id)
            
            # Savatni tozalash
            cart_items.delete()
            
            return JsonResponse({
                "success": True, 
                "message": "Buyurtma muvaffaqiyatli berildi",
                "order_ids": orders
            })
            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

# Eski OrderAddView o'rniga CheckoutView ishlatiladi
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