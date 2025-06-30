from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes
from utils import MINI_APP_URL


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler - Mini app tugmasini yuboradi"""
    user = update.effective_user

    # Mini app tugmasini yaratish
    keyboard = [
        [InlineKeyboardButton(
            text="🚀 Mini App ni ochish",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Xush kelibsiz xabari
    welcome_text = f"""
👋 Salom {user.first_name}!

🎮 Bizning mini app'ga xush kelibsiz!

Pastdagi tugmani bosing va mini app'ni oching:
    """

    await update.message.reply_text(
        text=welcome_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    help_text = """
📋 <b>Buyruqlar ro'yxati:</b>

/start - Botni ishga tushirish va mini app ochish
/help - Yordam olish
/app - Mini app'ni ochish

💡 Mini app'ni ochish uchun /start buyrug'ini yuboring!
    """

    await update.message.reply_text(
        text=help_text,
        parse_mode='HTML'
    )


async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """App command - Mini app tugmasini yuboradi"""
    keyboard = [
        [InlineKeyboardButton(
            text="🚀 Mini App",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text="🎮 Mini app'ni ochish uchun pastdagi tugmani bosing:",
        reply_markup=reply_markup
    )