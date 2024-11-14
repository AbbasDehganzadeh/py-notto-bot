import os
from dotenv import load_dotenv
from telebot import TeleBot, apihelper

from proxy import custom_proxy


load_dotenv()
bot = TeleBot(os.getenv("TOKEN"))
# setup custom proxy
apihelper.CUSTOM_REQUEST_SENDER = custom_proxy


@bot.message_handler(commands=["start"])
def greetUser(message):
    bot.send_message(message.chat.id, "Hello!")


@bot.message_handler(commands=["help"])
def greetUser(message):
    """It sends a short instruction."""
    bot.send_message(message.chat.id, "ربات تلگرامی سخن توشته شده با پایتون.")


bot.polling(interval=os.getEnv("interval"))
