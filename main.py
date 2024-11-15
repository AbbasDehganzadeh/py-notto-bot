import logging
import os

from dotenv import load_dotenv
from telebot import TeleBot, apihelper

from api_telegram_handler import get_all_quotes, get_random_item, search_quote
from api_translate import clean_author, translate
from proxy import custom_proxy

load_dotenv()
bot = TeleBot(os.getenv("TOKEN"))
# setup custom proxy
apihelper.CUSTOM_REQUEST_SENDER = custom_proxy


@bot.message_handler(commands=["start"])
def greetUser(message):
    """It gives a welcome to user"""
    bot.send_message(message.chat.id, "Hello {}!".format(message.from_user.first_name))


@bot.message_handler(commands=["random"])
def getRandomQuote(message):
    """It return a random qoute, with translation."""
    quotes = get_all_quotes()
    quote = get_random_item(quotes)

    tr_quote = dict()
    tr_quote["quote"] = translate(quote["quote"])
    tr_quote["person"] = translate(clean_author(quote["person"]))
    message_repl = f'{quote["person"]} says:\t\n{quote["quote"]}\n\n{tr_quote["person"]} میگه:\t\n{tr_quote["quote"]}'

    bot.reply_to(message, message_repl)


@bot.message_handler(commands=["help"])
def getHelp(message):
    """It sends a short instruction."""
    bot.send_message(
        message.chat.id,
        """ربات تلگرامی سخن توشته شده با پایتون:
    /start: شروع برنامه،
    /random: سخنان تصادفی،
    /help: طرز استفاده،
    `یک کلمه وارد کنید تا یک سخن تصادفی طبق آن کلمه دریافت کنید.`""",
    )


@bot.message_handler(func=lambda message: True)
def handleMessage(message):
    """It gets a keyword, and returns a random quote{person, quote} , based on that, with translation."""
    quotes = search_quote(message.text.strip())
    if len(quotes):
        quote = get_random_item(quotes)
        tr_quote = dict()
        tr_quote["quote"] = translate(quote["quote"])
        tr_quote["person"] = translate(clean_author(quote["person"]))
        message_repl = f'{quote["person"]} says:\t\n{quote["quote"]}\n\n{tr_quote["person"]} میگه:\t\n{tr_quote["quote"]}'
        bot.reply_to(message, message_repl)

    else: # or else no quote
        bot.reply_to(message, message.text + "\nno quote found``\\_(^-^)_/")


bot.polling(interval=10, logger_level=logging.DEBUG)
