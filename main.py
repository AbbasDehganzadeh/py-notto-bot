import logging
import os

from dotenv import load_dotenv
from telebot import TeleBot, apihelper

from api_telegram_handler import get_all_quotes, get_random_item, search_quote
from proxy import custom_proxy

load_dotenv()
bot = TeleBot(os.getenv("TOKEN"))
# setup custom proxy
apihelper.CUSTOM_REQUEST_SENDER = custom_proxy


@bot.message_handler(commands=["start"])
def greetUser(message):
    """It gives a welcome to user"""
    bot.send_message(message.chat.id, "Hello {}!".format(message.from_user.first_name))


@bot.message_handler(func=lambda message: True)
def handleMessage(message):
    """It gets a keyword, and returns a random quote{person, quote} , based on that."""
    quotes = search_quote(text.strip())
    if len(quotes):
        quote = get_random_item(quotes)
        bot.reply_to(message, '\n'.join([quote['person'], quote['person']]))

    # or else no quote
    bot.reply_to(message, message.text + "\nno quote found``\\_(^-^)_/")


@bot.message_handler(commands=["random"])
def greetUser(message):
    """It return a random qoute."""
    quotes = get_all_quotes()
    quote = get_random_item(quotes)

    bot.reply_to(message, '\n'.join([quote['person'], quote['person']]))


@bot.message_handler(commands=["help"])
def greetUser(message):
    """It sends a short instruction."""
    bot.send_message(
        message.chat.id,
        """ربات تلگرامی سخن توشته شده با پایتون:
    /start: شروع برنامه،
    /random: سخنان تصادفی،
    /help: طرز استفاده،
    `یک کلمه وارد کنید تا یک سخن تصادفی طبق آن کلمه دریافت کنید.`""",
    )


bot.polling(interval=os.getEnv("interval"), logger_level=logging.DEBUG)
