from aiogram.types import WebAppInfo, MenuButtonWebApp, MenuButtonDefault
from bot.config import WEBAPP_URL


async def setup_bot_menu(bot):
    try:
        if not WEBAPP_URL or not WEBAPP_URL.startswith("https://"):
            print(f"❌ URL noto'g'ri: {WEBAPP_URL}")
            return False

        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="🚀 Mini App", web_app=WebAppInfo(url=WEBAPP_URL)
            )
        )
        print(f"✅ Menu button o'rnatildi: {WEBAPP_URL}")
        return True
    except Exception as e:
        print(f"❌ Menu button xatolik: {e}")
        try:
            await bot.set_chat_menu_button(menu_button=MenuButtonDefault())
            print("⚠️ Default menu button o'rnatildi")
        except Exception as e2:
            print(f"❌ Default menu ham ishlamadi: {e2}")
        return False
