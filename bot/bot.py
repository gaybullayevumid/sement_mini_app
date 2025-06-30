import logging
from telegram.ext import Application, CommandHandler
from handlers import start, help_command, app_command
from utils import BOT_TOKEN

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Botni ishga tushirish"""
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handler'larni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("app", app_command))

    # Botni ishga tushirish
    print("🤖 Bot ishga tushirildi...")
    application.run_polling()


if __name__ == '__main__':
    main()