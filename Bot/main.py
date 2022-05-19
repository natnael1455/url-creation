import logging
import os

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.executor import start_webhook

API_TOKEN = int(os.getenv("bot_token"))

# webhook settings
WEBHOOK_HOST = "https://bot-35dnt5ajvq-lz.a.run.app"
WEBHOOK_PATH = "/api"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
print(WEBHOOK_URL)

# webserver settings
WEBAPP_HOST = "0.0.0.0"  # or ip
WEBAPP_PORT = int(os.getenv("PORT"))


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    web = WebAppInfo(url="https://url-creation.vercel.app/")
    button = InlineKeyboardButton("catalog", web_app=web)
    markup = InlineKeyboardMarkup()
    markup.add(button)
    return SendMessage(
        message.chat.id,
        "hi there, welcome.Here are the different catalogs",
        reply_markup=markup,
    )


@dp.message_handler()
async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id,)

    # or reply INTO webhook
    return SendMessage(message.chat.id, "to start use the /start command")


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning("Shutting down..")

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning("Bye!")


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
