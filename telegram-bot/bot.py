# import asyncio
import telegram
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import sys
import site
print(site.getsitepackages())
from python_telegram_bot import Updater, MessageHandler, Filters


TOKEN = "7067785400:AAEP8615N0p6UZU5YzFIEb1WLqRF4hX-Azg"


# Define a function to handle incoming messages.\venv\Scripts\activate
def reply_hello(update, context):
    # Reply with "Hello! How are you?"
    update.message.reply_text("Hello! How are you?")

def main():
    # Initialize the updater and dispatcher
    updater = Updater("YOUR_API_TOKEN_HERE", use_context=True)
    dp = updater.dispatcher

    # Add a message handler to reply to every message
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_hello))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
