import os
import django
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram import F

import asyncio

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()
from base.models import User

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
WEB_APP_URL = "https://your-domain.com/miniapp/"  # Mini app URL

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    telegram_user = message.from_user
    telegram_id = str(telegram_user.id)
    try:
        user = User.objects.get(telegram_id=telegram_id)
        if user.phone_number:
            await send_main_menu(message, user)
        else:
            await request_phone(message)
    except User.DoesNotExist:
        user = User.objects.create(
            telegram_id=telegram_id,
            first_name=telegram_user.first_name or '',
            last_name=telegram_user.last_name or '',
            username=telegram_user.username or ''
        )
        await request_phone(message)

async def request_phone(message: types.Message):
    kb = [
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
    ]
    await message.answer(
        "🔐 Ro'yxatdan o'tish uchun telefon raqamingizni yuboring:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
    )

@dp.message(F.contact)
async def handle_contact(message: types.Message):
    contact = message.contact
    telegram_id = str(message.from_user.id)
    if contact and contact.phone_number:
        try:
            user = User.objects.get(telegram_id=telegram_id)
            user.phone_number = contact.phone_number
            user.save()
            await message.answer(
                "✅ Telefon raqam muvaffaqiyatli saqlandi!\nEndi botdan foydalanishingiz mumkin.",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await send_main_menu(message, user)
        except User.DoesNotExist:
            await message.answer(
                "❌ Xatolik yuz berdi. Iltimos /start buyrug'ini qayta bosing."
            )

async def send_main_menu(message: types.Message, user: User):
    web_app = WebAppInfo(url=f"{WEB_APP_URL}?user_id={user.telegram_id}")
    kb = [
        [KeyboardButton(text="🛍️ Mini App ni ochish", web_app=web_app)],
        [KeyboardButton(text="👤 Profil"), KeyboardButton(text="ℹ️ Ma'lumot")]
    ]
    user_type_display = "Sotuvchi" if user.user_type == 'seller' else "Mijoz"
    first_name = user.first_name or ""
    await message.answer(
        f"👋 Xush kelibsiz, {first_name}!\n"
        f"📊 Status: {user_type_display}\n\n"
        f"Mini App orqali xizmatlardan foydalaning:",
        reply_markup=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    )

@dp.message(F.text == "👤 Profil")
async def profile(message: types.Message):
    telegram_id = str(message.from_user.id)
    try:
        user = User.objects.get(telegram_id=telegram_id)
        user_type_display = "Sotuvchi" if user.user_type == 'seller' else "Mijoz"
        first_name = user.first_name or ""
        last_name = user.last_name or ""
        phone_number = user.phone_number or ""
        created_at = user.created_at.strftime('%d.%m.%Y %H:%M') if user.created_at else ""
        profile_text = f"""
👤 <b>Profil ma'lumotlari:</b>

🏷️ Ism: {first_name}
🏷️ Familiya: {last_name}
📱 Telefon: {phone_number}
📊 Status: {user_type_display}
📅 Ro'yxatdan o'tgan: {created_at}
        """
        await message.answer(profile_text)
    except User.DoesNotExist:
        await message.answer(
            "❌ Foydalanuvchi topilmadi. /start buyrug'ini bosing."
        )

@dp.message(F.text == "ℹ️ Ma'lumot")
async def info(message: types.Message):
    await message.answer(
        "🤖 Bu bot orqali siz Mini App ga kirishingiz mumkin.\n"
        "Barcha funksiyalar Mini App ichida mavjud."
    )

@dp.message()
async def unknown(message: types.Message):
    await message.answer(
        "❓ Noma'lum buyruq. Iltimos menyudan tanlang."
    )

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))