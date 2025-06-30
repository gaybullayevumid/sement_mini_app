# Bot konfiguratsiyasi
BOT_TOKEN = "6667385868:AAEgEGKSM_YoHyGBAd2Xf4JwBt8tRwen6U8"
MINI_APP_URL = "https://your-domain.com/mini-app"

# Xabar shablonlari
WELCOME_MESSAGE = """
👋 Salom {first_name}!

🎮 Bizning mini app'ga xush kelibsiz!

Pastdagi tugmani bosing va mini app'ni oching:
"""

HELP_MESSAGE = """
📋 <b>Buyruqlar ro'yxati:</b>

/start - Botni ishga tushirish va mini app ochish
/help - Yordam olish
/app - Mini app'ni ochish

💡 Mini app'ni ochish uchun /start buyrug'ini yuboring!
"""

APP_MESSAGE = "🎮 Mini app'ni ochish uchun pastdagi tugmani bosing:"

# Tugma matnlari
BUTTON_TEXTS = {
    "open_app": "🚀 Mini App ni ochish",
    "mini_app": "🚀 Mini App"
}

# Utility funktsilar
def format_user_info(user):
    """Foydalanuvchi ma'lumotlarini formatlash"""
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username
    }

def log_user_action(user, action):
    """Foydalanuvchi harakatlarini loglash"""
    user_info = format_user_info(user)
    print(f"User {user_info['id']} ({user_info['first_name']}) performed: {action}")