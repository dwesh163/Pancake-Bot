from telegram.ext import Updater, CommandHandler
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

def startFunction(update, context):
    update.message.reply_text("Start")


def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    # Run bot
    updater.start_polling()

    # Stop bot with CTRL+C
    updater.idle()


if __name__ == '__main__':
    main()