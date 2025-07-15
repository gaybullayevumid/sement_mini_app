from aiogram import Bot, Dispatcher, types
from asyncio import run

dp = Dispatcher()

async def startup_answer(bot: Bot):
    await bot.send_message(5323321097, "Bot ishga tushdi!✅")

async def shutdown_answer(bot: Bot):
    await bot.send_message(5323321097, "Bot ishdan toxtadi! ❌")

async def echo(message: types.Message, bot: Bot):
    await message.copy_to(chat_id=message.chat.id)

async def start():
    dp.startup.register(startup_answer)
    dp.message.register(echo)
    dp.shutdown.register(shutdown_answer)

    bot = Bot("7714575462:AAE88sVMe9_NsfZ1fBSEeOjqCSy1iOe2Lwo")
    await dp.start_polling(bot, polling_timeout=1)

run(start())