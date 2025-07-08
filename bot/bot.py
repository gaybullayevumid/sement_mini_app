# telegram_bot.py
import asyncio
import aiohttp
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Bot token
BOT_TOKEN = "6667385868:AAEgEGKSM_YoHyGBAd2Xf4JwBt8tRwen6U8"
API_URL = "http://localhost:8000/api"

# Logging
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# FSM holatlari
class UserRegistration(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_phone = State()

# Telefon raqam tugmasi
phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Django API bilan bog'lanish
async def send_user_data(user_data):
    """User ma'lumotlarini Django API ga yuborish"""
    try:
        async with aiohttp.ClientSession() as session:
            logging.info(f"Sending data to API: {user_data}")
            async with session.post(f"{API_URL}/users/create/", json=user_data) as response:
                response_text = await response.text()
                logging.info(f"API Response status: {response.status}")
                logging.info(f"API Response body: {response_text}")
                
                if response.status == 201:
                    return await response.json()
                else:
                    logging.error(f"API error: {response.status} - {response_text}")
                    return None
    except aiohttp.ClientError as e:
        logging.error(f"Network error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

# API bilan bog'lanishni tekshirish
async def check_api_health():
    """API ishlayotganini tekshirish"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/health/") as response:
                if response.status == 200:
                    logging.info("API is healthy")
                    return True
                else:
                    logging.error(f"API health check failed: {response.status}")
                    return False
    except Exception as e:
        logging.error(f"API health check error: {e}")
        return False

# /start komandasi
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    # Avval API ishlayotganini tekshiramiz
    api_healthy = await check_api_health()
    if not api_healthy:
        await message.answer(
            "Kechirasiz, hozirda xizmat vaqtincha mavjud emas. "
            "Iltimos, keyinroq qayta urinib ko'ring."
        )
        return
    
    await message.answer(
        "Salom! Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak.\n\n"
        "Iltimos, ismingizni kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserRegistration.waiting_for_name)

# Ism qabul qilish
@dp.message(UserRegistration.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Iltimos, ismingizni kiriting:")
        return
    
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Ism kamida 2 ta belgidan iborat bo'lishi kerak. Qayta kiriting:")
        return
    
    await state.update_data(first_name=name)
    await message.answer("Familiyangizni kiriting:")
    await state.set_state(UserRegistration.waiting_for_surname)

# Familiya qabul qilish
@dp.message(UserRegistration.waiting_for_surname)
async def process_surname(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Iltimos, familiyangizni kiriting:")
        return
    
    surname = message.text.strip()
    if len(surname) < 2:
        await message.answer("Familiya kamida 2 ta belgidan iborat bo'lishi kerak. Qayta kiriting:")
        return
    
    await state.update_data(last_name=surname)
    await message.answer(
        "Telefon raqamingizni yuboring:",
        reply_markup=phone_keyboard
    )
    await state.set_state(UserRegistration.waiting_for_phone)

# Telefon raqam validatsiyasi
def validate_phone(phone: str) -> bool:
    """Telefon raqamni validatsiya qilish"""
    import re
    if not phone:
        return False
    
    # Telefon raqam faqat raqamlar va + belgisidan iborat bo'lishi kerak
    phone_pattern = re.compile(r'^\+?[1-9]\d{1,14}$')
    return bool(phone_pattern.match(phone.replace(' ', '').replace('-', '')))

# Telefon raqam qabul qilish
@dp.message(UserRegistration.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone_number = None
    
    if message.contact:
        phone_number = message.contact.phone_number
    elif message.text:
        phone_number = message.text.strip()
    
    if not phone_number:
        await message.answer("Iltimos, telefon raqamingizni yuboring yoki tugmani bosing.")
        return
    
    # Telefon raqamni formatlash
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    
    # Validatsiya
    if not validate_phone(phone_number):
        await message.answer(
            "Telefon raqam noto'g'ri formatda. Iltimos, to'g'ri formatda kiriting "
            "(masalan: +998901234567 yoki tugmani bosing):"
        )
        return
    
    # Ma'lumotlarni yig'ish
    user_data = await state.get_data()
    user = message.from_user
    
    if not user:
        await message.answer("Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        await state.clear()
        return
    
    user_data.update({
        'telegram_id': str(user.id),  # String sifatida yuborish
        'username': user.username if user.username else '',
        'phone_number': phone_number
    })
    
    # Django API ga yuborish
    await message.answer("Ma'lumotlar saqlanmoqda... ⏳")
    result = await send_user_data(user_data)
    
    if result:
        await message.answer(
            f"Ro'yxatdan o'tish muvaffaqiyatli yakunlandi! ✅\n\n"
            f"Ism: {user_data.get('first_name', '')}\n"
            f"Familiya: {user_data.get('last_name', '')}\n"
            f"Telefon: {user_data.get('phone_number', '')}",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "Xatolik yuz berdi. Bu telegram ID allaqachon ro'yxatdan o'tgan bo'lishi mumkin "
            "yoki server bilan bog'lanishda muammo bor. Iltimos, qayta urinib ko'ring.",
            reply_markup=ReplyKeyboardRemove()
        )
    
    await state.clear()

# Mini App tugmasi
@dp.message(Command("app"))
async def cmd_app(message: types.Message):
    # Mini App tugmasi
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="🚀 Mini App ochish",
            web_app=types.WebAppInfo(url="https://your-mini-app-url.com")
        )]
    ])
    await message.answer("Mini App ni ochish uchun tugmani bosing:", reply_markup=keyboard)

# Debug komandasi
@dp.message(Command("debug"))
async def cmd_debug(message: types.Message):
    """Debug ma'lumotlarini ko'rish"""
    user = message.from_user
    if not user:
        await message.answer("Foydalanuvchi ma'lumotlari topilmadi.")
        return
    
    await message.answer(
        f"Debug Ma'lumotlar:\n"
        f"User ID: {user.id}\n"
        f"Username: {user.username if user.username else 'N/A'}\n"
        f"First Name: {user.first_name if user.first_name else 'N/A'}\n"
        f"Last Name: {user.last_name if user.last_name else 'N/A'}\n"
        f"API URL: {API_URL}"
    )

# Asosiy funksiya
async def main():
    try:
        logging.info("Bot started")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())