import logging
import os
import requests
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

FIRSTNAME, LASTNAME, PHONE = range(3)

API_URL = "http://sementsavdo.uz/swagger/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("Ismingizni kiriting:")
        return FIRSTNAME

async def get_firstname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and context.user_data is not None:
        context.user_data["first_name"] = update.message.text
        await update.message.reply_text("Familiyangizni kiriting:")
        return LASTNAME
    else:
        return ConversationHandler.END

async def get_lastname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and context.user_data is not None:
        context.user_data["last_name"] = update.message.text
        await update.message.reply_text(
            "Telefon raqamingizni kiriting (masalan: 998901234567):"
        )
        return PHONE
    else:
        return ConversationHandler.END

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and context.user_data is not None:
        phone = update.message.text
        context.user_data["phone"] = phone
        user_id = ""
        if update.message.from_user and hasattr(update.message.from_user, "id"):
            user_id = str(update.message.from_user.id)
        else:
            user_id = ""
        data = {
            "username": user_id,
            "first_name": context.user_data.get("first_name", ""),
            "last_name": context.user_data.get("last_name", ""),
            "phone": phone,
            "user_type": "client",
        }
        try:
            r = requests.post(API_URL, json=data)
            if r.status_code in [200, 201]:
                await update.message.reply_text(
                    "Ma'lumotlaringiz saqlandi! Endi buyurtma bera olasiz.",
                    reply_markup=ReplyKeyboardRemove(),
                )
            else:
                await update.message.reply_text(
                    f"Xatolik! (kod: {r.status_code})\nQaytadan urinib ko‘ring.",
                    reply_markup=ReplyKeyboardRemove(),
                )
        except Exception as e:
            await update.message.reply_text(
                f"Server bilan bog‘lanishda xatolik: {e}", reply_markup=ReplyKeyboardRemove()
            )
        return ConversationHandler.END
    else:
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("Bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    TOKEN = "6667385868:AAEgEGKSM_YoHyGBAd2Xf4JwBt8tRwen6U8"
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRSTNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_firstname)],
            LASTNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_lastname)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    print('Bot ishga tushdi...')
    application.run_polling()

if __name__ == '__main__':
    main()