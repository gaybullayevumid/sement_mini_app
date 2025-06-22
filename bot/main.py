import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.handlers.start import router
from bot.handlers.webapp import setup_bot_menu
from bot.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await setup_bot_menu(bot)
    print("🚀 Bot ishga tushmoqda...")

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Botda xatolik: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
