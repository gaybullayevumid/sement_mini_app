from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from bot.config import WEBAPP_URL

def get_main_keyboard(debug=False, back_button=False):
    buttons = [
        [
            InlineKeyboardButton(
                text="🚀 Mini App ochish",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]
    ]

    if debug:
        buttons.append([
            InlineKeyboardButton(
                text="🔄 Menu Button yangilash",
                callback_data="refresh_menu"
            )
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                text="ℹ️ Yordam",
                callback_data="help"
            )
        ])

    if back_button:
        buttons.append([
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="back_to_start"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
