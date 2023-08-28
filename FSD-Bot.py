from telegram.ext import Updater, CommandHandler
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

def startFunction(update, context):
    update.message.reply_text("Start")

def helpFunction(update, context):
    update.message.reply_text("help")

def brainFunction(update, context):
    update.message.reply_text("brain")

def smartFunction(update, context):
    update.message.reply_text("smart")

def codeFunction(update, context):
    update.message.reply_text("code")

def geekFunction(update, context):
    update.message.reply_text("geek")

def alienFunction(update, context):
    update.message.reply_text("alien")

def drinkFunction(update, context):
    update.message.reply_text("drink")

def coffeeFunction(update, context):
    update.message.reply_text("coffee")

def beerFunction(update, context):
    update.message.reply_text("beer")

def drinkSomethingFunction(update, context):
    update.message.reply_text("drink Something")


def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    # Base Command
    dp.add_handler(CommandHandler("start", startFunction))
    dp.add_handler(CommandHandler("help", helpFunction))

    # Print Command
    dp.add_handler(CommandHandler("brain", brainFunction))
    dp.add_handler(CommandHandler("smart", smartFunction))

    dp.add_handler(CommandHandler("code", codeFunction))
    dp.add_handler(CommandHandler("geek", geekFunction))

    dp.add_handler(CommandHandler("alien", alienFunction))
    dp.add_handler(CommandHandler("geek", geekFunction))

    dp.add_handler(CommandHandler("drink", drinkFunction))
    dp.add_handler(CommandHandler("coffee", coffeeFunction))
    dp.add_handler(CommandHandler("beer", beerFunction))
    dp.add_handler(CommandHandler("drink_something", drinkSomethingFunction))

    # Run bot
    updater.start_polling()

    # Stop bot with CTRL+C
    updater.idle()


if __name__ == '__main__':
    main()