from aiogram import types, Router, F
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from bot.config import WEBAPP_URL
from bot.keyboards.default import get_main_keyboard
from bot.handlers.webapp import setup_bot_menu
import logging

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message):
    menu_success = False
    try:
        menu_success = await setup_bot_menu(message.bot)
    except Exception as e:
        logging.error(f"Menu button sozlashda xatolik: {e}")

    menu_status = (
        "💡 <i>Shuningdek, pastdagi menu tugmasidan ham foydalanishingiz mumkin!</i>"
        if menu_success
        else "⚠️ <i>Menu button hozircha ishlamayapti, inline tugmadan foydalaning.</i>"
    )

    await message.answer(
        f"Salom {message.from_user.first_name}! 👋\n\n"
        "Bu Hello World Mini App boti.\n"
        "Quyidagi tugma orqali mini appni oching:\n\n"
        f"{menu_status}",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "help")
async def help_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📱 <b>Mini App haqida:</b>\n\n"
        "• Bu oddiy Hello World dasturi\n"
        "• Django bilan yaratilgan\n"
        "• Telegram Web App texnologiyasi ishlatilgan\n\n"
        "Mini appni ochish uchun tugmani bosing! 👇\n\n"
        "💡 <i>Agar menu button ishlamasa, inline tugmadan foydalaning.</i>",
        parse_mode="HTML",
        reply_markup=get_main_keyboard(back_button=True),
    )


@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"Salom {callback.from_user.first_name}! 👋\n\n"
        "Bu Hello World Mini App boti.\n"
        "Quyidagi tugma orqali mini appni oching:\n\n"
        "💡 <i>Inline tugma ishonchli ishlaydi!</i>",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML",
    )


@router.message(Command("debug"))
async def debug_command(message: types.Message):
    from bot.config import WEBAPP_URL

    debug_info = f"""
🔍 <b>Debug Ma'lumotlari:</b>

📱 <b>Bot ID:</b> {message.bot.id}
🌐 <b>WEBAPP_URL:</b> <code>{WEBAPP_URL}</code>
✅ <b>URL Format:</b> {'To\'g\'ri' if WEBAPP_URL.startswith('https://') else 'Noto\'g\'ri - https:// kerak'}
🔗 <b>URL Uzunligi:</b> {len(WEBAPP_URL)}

<b>Holat:</b>
• Inline button: ✅ Ishlaydi
• Menu button: ❓ Test qilib ko'ring

<b>Agar menu button ishlamasa:</b>
1. Ngrok yangi URL berganmi?
2. Config.py yangilangami?
3. Bot qayta ishga tushirilganmi?
    """
    await message.answer(
        debug_info, parse_mode="HTML", reply_markup=get_main_keyboard(debug=True)
    )


@router.callback_query(F.data == "refresh_menu")
async def refresh_menu_callback(callback: types.CallbackQuery):
    success = await setup_bot_menu(callback.bot)
    status = (
        "✅ Menu button muvaffaqiyatli yangilandi!"
        if success
        else "❌ Menu button yangilanmadi. URL ni tekshiring."
    )
    await callback.answer(status, show_alert=True)


@router.message()
async def echo_handler(message: types.Message):
    if "mini app" in message.text.lower() or "ochish" in message.text.lower():
        await message.answer(
            "Mini appni ochish uchun quyidagi tugmani bosing:\n\n"
            "💡 <i>Inline tugma ishonchli ishlaydi!</i>",
            reply_markup=get_main_keyboard(),
            parse_mode="HTML",
        )
    else:
        await message.answer(
            "Mini appni ishlatish uchun /start buyrug'ini yuboring! 🚀\n\n"
            "🔧 <i>Debug uchun /debug buyrug'ini yuboring</i>",
            parse_mode="HTML",
        )
