import logging
import os

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)
from aiogram.utils.executor import start_webhook

API_TOKEN = os.getenv("BotToken")
# webhook settings
WEBHOOK_HOST = os.getenv("WebHook")
WEBHOOK_PATH = "/api"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver setting
WEBAPP_HOST = "0.0.0.0"  # or ip
WEBAPP_PORT = int(os.getenv("PORT"))


logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    web = WebAppInfo(url="https://url-creation.vercel.app/")
    button = InlineKeyboardButton("catalog", web_app=web)
    button2 = KeyboardButton("catalog", web_app=web)
    markup = InlineKeyboardMarkup()
    kmarkup = ReplyKeyboardMarkup()
    markup.add(button)
    kmarkup.add(button2)
    logging.debug("message received")
    return SendMessage(
        message.chat.id,
        "hi there, welcome.Here are the different catalogs",
        reply_markup=kmarkup,
    )


@dp.message_handler()
async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id,)
    # or reply INTO webhook
    # print(message.web_app_data.data)
    logging.info(message.text)
    return SendMessage(message.chat.id, message.chat.id)


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
