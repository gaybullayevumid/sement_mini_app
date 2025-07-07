# from aiogram import types
# from aiogram.fsm.context import FSMContext
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# from django.db import IntegrityError
# from base.models import Seller, Client
# import re

# # States for seller registration
# from aiogram.fsm.state import State, StatesGroup

# class SellerRegistration(StatesGroup):
#     business_name = State()
#     first_name = State()
#     last_name = State()
#     phone_number = State()
#     address = State()
#     confirmation = State()

# # Seller registration handlers
# async def start_seller_registration(message: types.Message, state: FSMContext):
#     user = message.from_user

#     try:
#         seller = Seller.objects.get(telegram_id=str(user.id))
#         if seller.is_active:
#             await message.answer(
#                 f"Siz allaqachon ro'yxatdan o'tgansiz!\n"
#                 f"Biznes nomi: {seller.business_name}\n"
#                 f"Telefon: {seller.phone_number}"
#             )
#             return
#     except Seller.DoesNotExist:
#         pass

#     await message.answer(
#         f"Assalomu alaykum {user.first_name}!\n"
#         f"Sotuvchi sifatida ro'yxatdan o'tish uchun ma'lumotlaringizni to'ldiring.\n\n"
#         f"Biznes nomingizni kiriting:"
#     )
#     await state.set_state(SellerRegistration.business_name)

# async def get_business_name(message: types.Message, state: FSMContext):
#     business_name = message.text.strip()
#     if len(business_name) < 2:
#         await message.answer("Biznes nomi kamida 2 ta belgidan iborat bo'lishi kerak. Qaytadan kiriting:")
#         return

#     await state.update_data(business_name=business_name)
#     await message.answer(f"Biznes nomi: {business_name}\n\nEndi ismingizni kiriting:")
#     await state.set_state(SellerRegistration.first_name)

# async def get_first_name(message: types.Message, state: FSMContext):
#     first_name = message.text.strip()
#     if len(first_name) < 2:
#         await message.answer("Ism kamida 2 ta belgidan iborat bo'lishi kerak. Qaytadan kiriting:")
#         return

#     await state.update_data(first_name=first_name)
#     await message.answer(
#         f"Ism: {first_name}\n\nFamiliyangizni kiriting (ixtiyoriy, o'tkazib yuborish uchun /skip yozing):"
#     )
#     await state.set_state(SellerRegistration.last_name)

# async def get_last_name(message: types.Message, state: FSMContext):
#     last_name = message.text.strip()
#     if last_name.lower() == '/skip':
#         last_name = ''

#     await state.update_data(last_name=last_name)

#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[[KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]],
#         resize_keyboard=True,
#         one_time_keyboard=True
#     )

#     await message.answer(
#         "Telefon raqamingizni yuboring.\n"
#         "Quyidagi tugmani bosing yoki raqamni qo'lda kiriting (+998XXXXXXXXX formatida):",
#         reply_markup=keyboard
#     )
#     await state.set_state(SellerRegistration.phone_number)

# async def get_phone_number(message: types.Message, state: FSMContext):
#     if message.contact:
#         phone_number = message.contact.phone_number
#     else:
#         phone_number = message.text.strip()
#         phone_pattern = r'^\+998\d{9}$'
#         if not re.match(phone_pattern, phone_number):
#             await message.answer("Telefon raqam noto'g'ri formatda. +998XXXXXXXXX formatida kiriting.\nMasalan: +998901234567")
#             return

#     await state.update_data(phone_number=phone_number)
#     await message.answer("Telefon: {}\n\nManzil (to'liq manzil) kiriting:".format(phone_number), reply_markup=ReplyKeyboardRemove())
#     await state.set_state(SellerRegistration.address)

# async def get_address(message: types.Message, state: FSMContext):
#     address = message.text.strip()
#     if len(address) < 10:
#         await message.answer("Manzil kamida 10 ta belgidan iborat bo'lishi kerak. Qaytadan kiriting:")
#         return

#     await state.update_data(address=address)
#     user_data = await state.get_data()

#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="✅ Tasdiqlash")],
#             [KeyboardButton(text="❌ Bekor qilish")]
#         ],
#         resize_keyboard=True,
#         one_time_keyboard=True
#     )

#     confirmation_text = (
#         f"Ma'lumotlaringizni tasdiqlang:\n\n"
#         f"👤 Ism: {user_data['first_name']}\n"
#         f"👥 Familiya: {user_data.get('last_name', 'Ko‘rsatilmagan')}\n"
#         f"🏢 Biznes nomi: {user_data['business_name']}\n"
#         f"📞 Telefon: {user_data['phone_number']}\n"
#         f"📍 Manzil: {address}\n\n"
#         f"Tasdiqlash uchun tugmani bosing:"
#     )

#     await message.answer(confirmation_text, reply_markup=keyboard)
#     await state.set_state(SellerRegistration.confirmation)

# async def confirm_registration(message: types.Message, state: FSMContext):
#     if message.text == "❌ Bekor qilish":
#         await cancel_registration(message, state)
#         return

#     if message.text != "✅ Tasdiqlash":
#         await message.answer("Iltimos tugmalardan birini tanlang:")
#         return

#     user = message.from_user
#     user_data = await state.get_data()

#     try:
#         seller = Seller.objects.create(
#             telegram_id=str(user.id),
#             telegram_username=user.username or '',
#             first_name=user_data['first_name'],
#             last_name=user_data.get('last_name', ''),
#             business_name=user_data['business_name'],
#             phone_number=user_data['phone_number'],
#             address=user_data['address'],
#             is_active=True
#         )

#         await message.answer(
#             f"🎉 Tabriklaymiz!\nSiz muvaffaqiyatli ro'yxatdan o'tdingiz.\n\n"
#             f"Biznes ID: {seller.id}\n"
#             f"Biznes nomi: {seller.business_name}\n\n"
#             f"Endi siz mahsulotlaringizni qo'sha boshlashingiz mumkin!",
#             reply_markup=ReplyKeyboardRemove()
#         )
#         await state.clear()

#     except IntegrityError:
#         await message.answer("❌ Xatolik: Siz allaqachon ro'yxatdan o'tgansiz!", reply_markup=ReplyKeyboardRemove())
#         await state.clear()
#     except Exception as e:
#         await message.answer(f"❌ Ro'yxatdan o'tishda xatolik yuz berdi: {str(e)}\nIltimos qaytadan urinib ko'ring.", reply_markup=ReplyKeyboardRemove())
#         await state.clear()

# async def cancel_registration(message: types.Message, state: FSMContext):
#     await state.clear()
#     await message.answer(
#         "❌ Ro'yxatdan o'tish bekor qilindi.\nQaytadan boshlash uchun /register_seller buyrug'ini ishlating.",
#         reply_markup=ReplyKeyboardRemove()
#     )

# async def seller_profile(message: types.Message):
#     user = message.from_user
#     try:
#         seller = Seller.objects.get(telegram_id=str(user.id))
#         profile_text = (
#             f"👤 Sizning profilingiz:\n\n"
#             f"🆔 ID: {seller.id}\n"
#             f"👤 Ism: {seller.first_name} {seller.last_name}\n"
#             f"🏢 Biznes: {seller.business_name}\n"
#             f"📞 Telefon: {seller.phone_number}\n"
#             f"📍 Manzil: {seller.address}\n"
#             f"📅 Ro'yxatdan o'tgan: {seller.created_at.strftime('%d.%m.%Y')}\n"
#             f"📊 Status: {'Faol' if seller.is_active else 'Faol emas'}\n"
#             f"📦 Mahsulotlar soni: {seller.products.count()}"
#         )
#         await message.answer(profile_text)
#     except Seller.DoesNotExist:
#         await message.answer("❌ Siz hali ro'yxatdan o'tmagansiz.\nRo'yxatdan o'tish uchun /register_seller buyrug'ini ishlating.")

# # Client registration
# async def start_client_registration(message: types.Message, state: FSMContext = None):
#     user = message.from_user
#     try:
#         client = Client.objects.get(telegram_id=str(user.id))
#         if client.is_active:
#             await message.answer(
#                 f"Siz allaqachon ro'yxatdan o'tgansiz!\n"
#                 f"Ism: {client.first_name}\n"
#                 f"Username: @{client.telegram_username or 'N/A'}\n\n"
#                 f"Buyruqlar:\n/products - Mahsulotlar\n/cart - Savat\n/orders - Buyurtmalar\n/register_seller - Sotuvchi bo'lish"
#             )
#             return
#     except Client.DoesNotExist:
#         pass

#     try:
#         client = Client.objects.create(
#             telegram_id=str(user.id),
#             telegram_username=user.username or '',
#             first_name=user.first_name or 'User',
#             last_name=user.last_name or '',
#             is_active=True
#         )

#         await message.answer(
#             f"🎉 Xush kelibsiz!\nSiz muvaffaqiyatli ro'yxatdan o'tdingiz.\n\n"
#             f"Ism: {client.first_name}\n"
#             f"Endi mahsulotlarni ko'rish va buyurtma berishingiz mumkin!\n\n"
#             f"Buyruqlar:\n/products - Mahsulotlar\n/cart - Savat\n/orders - Buyurtmalar\n/register_seller - Sotuvchi bo'lish"
#         )

#     except IntegrityError:
#         await message.answer("❌ Xatolik: Siz allaqachon ro'yxatdan o'tgansiz!")
#     except Exception as e:
#         await message.answer(f"❌ Ro'yxatdan o'tishda xatolik yuz berdi: {str(e)}")

# # Help command
# async def help_command(message: types.Message, state: FSMContext = None):
#     help_text = (
#         "🤖 Bot buyruqlari:\n\n"
#         "👥 Umumiy:\n"
#         "/start - Botni boshlash\n"
#         "/help - Yordam\n"
#         "/register_seller - Sotuvchi sifatida ro'yxatdan o'tish\n"
#         "/profile - Profil\n\n"
#         "🛍️ Mijozlar uchun:\n"
#         "/products - Mahsulotlar\n"
#         "/cart - Savat\n"
#         "/orders - Buyurtmalar\n\n"
#         "🏪 Sotuvchilar uchun:\n"
#         "/add_product - Mahsulot qo'shish\n"
#         "/my_products - Mening mahsulotlarim\n"
#         "/my_orders - Mening buyurtmalarim"
#     )
#     await message.answer(help_text)

# # Matnli xabarlarni qayta ishlash
# from utils import get_main_keyboard

# async def handle_text_messages(message: types.Message, state: FSMContext):
#     text = message.text

#     if text == "🏪 Sotuvchi bo'lish":
#         await start_seller_registration(message, state)
#     elif text == "👤 Profil":
#         await seller_profile(message)
#     elif text == "ℹ️ Yordam":
#         await help_command(message)
#     else:
#         await message.answer(
#             "Noma'lum buyruq. Yordam uchun /help buyrug'ini ishlating.",
#             reply_markup=get_main_keyboard()
#         )