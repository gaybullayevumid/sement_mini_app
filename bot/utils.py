# import re
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from base.models import Seller, Client, Order

# def is_seller(telegram_id):
#     try:
#         seller = Seller.objects.get(telegram_id=str(telegram_id), is_active=True)
#         return seller
#     except Seller.DoesNotExist:
#         return None

# def is_client(telegram_id):
#     try:
#         client = Client.objects.get(telegram_id=str(telegram_id), is_active=True)
#         return client
#     except Client.DoesNotExist:
#         return None

# def get_user_type(telegram_id):
#     seller = is_seller(telegram_id)
#     if seller:
#         return 'seller', seller
#     client = is_client(telegram_id)
#     if client:
#         return 'client', client
#     return None, None

# def get_main_keyboard():
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="🛍️ Mahsulotlar"), KeyboardButton(text="🛒 Savat")],
#             [KeyboardButton(text="📦 Buyurtmalar"), KeyboardButton(text="👤 Profil")],
#             [KeyboardButton(text="🏪 Sotuvchi bo'lish"), KeyboardButton(text="ℹ️ Yordam")]
#         ],
#         resize_keyboard=True,
#         one_time_keyboard=False
#     )
#     return keyboard

# def get_seller_keyboard():
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="➕ Mahsulot qo'shish"), KeyboardButton(text="📦 Mening mahsulotlarim")],
#             [KeyboardButton(text="📋 Buyurtmalar"), KeyboardButton(text="📊 Statistika")],
#             [KeyboardButton(text="👤 Profil"), KeyboardButton(text="ℹ️ Yordam")]
#         ],
#         resize_keyboard=True,
#         one_time_keyboard=False
#     )
#     return keyboard

# def get_admin_keyboard():
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="👥 Foydalanuvchilar"), KeyboardButton(text="🏪 Sotuvchilar")],
#             [KeyboardButton(text="📦 Barcha mahsulotlar"), KeyboardButton(text="📋 Barcha buyurtmalar")],
#             [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="⚙️ Sozlamalar")]
#         ],
#         resize_keyboard=True,
#         one_time_keyboard=False
#     )
#     return keyboard

# def format_product_info(product):
#     return (
#         f"🏷️ <b>{product.name}</b>\n"
#         f"🏭 Brand: {product.brand}\n"
#         f"📦 Tur: {product.type}\n"
#         f"⭐ Sifat: {product.quality}\n"
#         f"⚖️ Og'irlik: {product.weight} kg\n"
#         f"🌍 Kelib chiqishi: {product.origin}\n"
#         f"🏗️ Sement sinfi: {product.cement_class}\n"
#         f"💰 Narx: <b>{product.price:,} so'm</b>\n"
#         f"📊 Mavjud: {'✅ Ha' if product.is_available else '❌ Yo‘q'}\n"
#         f"🏢 Sotuvchi: {product.seller.business_name}\n"
#         f"📞 Telefon: {product.seller.phone_number}"
#     )

# def format_order_info(order):
#     status_emoji = {
#         'pending': '⏳',
#         'confirmed': '✅',
#         'processing': '🔄',
#         'shipped': '🚚',
#         'delivered': '✅',
#         'cancelled': '❌'
#     }
#     return (
#         f"📋 <b>Buyurtma #{order.order_number}</b>\n"
#         f"📅 Sana: {order.date.strftime('%d.%m.%Y %H:%M')}\n"
#         f"👤 Mijoz: {order.client.first_name}\n"
#         f"📦 Mahsulot: {order.product.name}\n"
#         f"📊 Miqdor: {order.quantity}\n"
#         f"💰 Jami: <b>{order.total_price:,} so'm</b>\n"
#         f"📍 Status: {status_emoji.get(order.status, '❓')} {dict(order.STATUS_CHOICES)[order.status]}\n"
#         f"📞 Telefon: {order.client_phone or 'N/A'}\n"
#         f"📍 Manzil: {order.client_address or 'N/A'}"
#     )

# def get_product_inline_keyboard(product_id, is_seller=False):
#     buttons = []
#     if is_seller:
#         buttons.extend([
#             [InlineKeyboardButton(text="✏️ Tahrirlash", callback_data=f"edit_product_{product_id}")],
#             [InlineKeyboardButton(text="🗑️ O'chirish", callback_data=f"delete_product_{product_id}")],
#             [InlineKeyboardButton(text="📊 Statistika", callback_data=f"product_stats_{product_id}")]
#         ])
#     else:
#         buttons.extend([
#             [InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data=f"add_to_cart_{product_id}")],
#             [InlineKeyboardButton(text="📞 Sotuvchiga bog'lanish", callback_data=f"contact_seller_{product_id}")]
#         ])
#     return InlineKeyboardMarkup(inline_keyboard=buttons)

# def get_order_inline_keyboard(order_id, user_type):
#     buttons = []
#     if user_type == 'seller':
#         buttons.extend([
#             [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_order_{order_id}")],
#             [InlineKeyboardButton(text="🔄 Tayyorlanmoqda", callback_data=f"process_order_{order_id}")],
#             [InlineKeyboardButton(text="🚚 Yetkazilmoqda", callback_data=f"ship_order_{order_id}")],
#             [InlineKeyboardButton(text="✅ Yetkazildi", callback_data=f"deliver_order_{order_id}")],
#             [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_order_{order_id}")]
#         ])
#     else:
#         buttons.extend([
#             [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_order_{order_id}")],
#             [InlineKeyboardButton(text="📞 Sotuvchiga bog'lanish", callback_data=f"contact_seller_order_{order_id}")]
#         ])
#     return InlineKeyboardMarkup(inline_keyboard=buttons)

# def get_cart_inline_keyboard(cart_item_id):
#     buttons = [
#         [
#             InlineKeyboardButton(text="➖", callback_data=f"cart_decrease_{cart_item_id}"),
#             InlineKeyboardButton(text="➕", callback_data=f"cart_increase_{cart_item_id}")
#         ],
#         [InlineKeyboardButton(text="🗑️ O'chirish", callback_data=f"cart_remove_{cart_item_id}")],
#         [InlineKeyboardButton(text="📦 Buyurtma berish", callback_data=f"order_from_cart_{cart_item_id}")]
#     ]
#     return InlineKeyboardMarkup(inline_keyboard=buttons)

# def get_pagination_keyboard(page, total_pages, callback_prefix):
#     buttons = []
#     page_buttons = []
#     if page > 1:
#         page_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"{callback_prefix}_{page-1}"))
#     page_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="current_page"))
#     if page < total_pages:
#         page_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"{callback_prefix}_{page+1}"))
#     buttons.append(page_buttons)
#     return InlineKeyboardMarkup(inline_keyboard=buttons)

# def validate_phone_number(phone):
#     phone_pattern = r'^\+998\d{9}$'
#     return re.match(phone_pattern, phone) is not None

# def format_price(price):
#     return f"{price:,} so'm"

# def get_user_stats(user_id, user_type):
#     if user_type == 'seller':
#         try:
#             seller = Seller.objects.get(telegram_id=str(user_id))
#             total_products = seller.products.count()
#             active_products = seller.products.filter(is_available=True).count()
#             total_orders = Order.objects.filter(seller=seller).count()
#             pending_orders = Order.objects.filter(seller=seller, status='pending').count()

#             return {
#                 'total_products': total_products,
#                 'active_products': active_products,
#                 'total_orders': total_orders,
#                 'pending_orders': pending_orders
#             }
#         except Seller.DoesNotExist:
#             return None
#     elif user_type == 'client':
#         try:
#             client = Client.objects.get(telegram_id=str(user_id))
#             # Faqat related_name='cart_items' ishlaydi
#             cart_items = client.cart_items.count()
#             total_orders = Order.objects.filter(client=client).count()
#             return {
#                 'total_orders': total_orders,
#                 'cart_items': cart_items
#             }
#         except Client.DoesNotExist:
#             return None
#     return None