from telegram.ext import Updater, CommandHandler
import os
from dotenv import load_dotenv
from dictionary import messageDictionary, brainEmojiDictionary, codeEmojiDictionary, alienEmojiDictionary
from random import *
import json
from datetime import datetime

load_dotenv()

TOKEN = os.getenv('TOKEN')

global geek
geek = 0

def sendEmoji(user, text, update, context):

    path = "data.json"
    newUser = 1
    number = randint(1,5)

    if text == "brain" or text == "smart":
        text1 = "brain"
        text2 = "smart"
        EmojiDictionary = brainEmojiDictionary
    
    if text == "code" or text == "geek":
        text1 = "code"
        text2 = "geek"
        EmojiDictionary = codeEmojiDictionary

    if text == "geek" or text == "alien":
        text1 = "geek"
        text2 = "alien"
        EmojiDictionary = alienEmojiDictionary


    username = user['username']
    userID = user['id']

    with open(path, 'r') as jsonFile:
        data = json.load(jsonFile)

    for i in range(len(data)):
        if data[i]["id"] == userID:
            if data[i]["text"] == text1 or data[i]["text"] == text2:
                update.message.reply_text("Une seule commande par utilisateur est autorisée par jour")
                newUser = 0
            
        
    
    if newUser == 1:
        print(f"new User : {username} ")
        dictionary = {
            "username": username,
            "id": userID,
            "text": text,
            "number": number,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%m/%d/%y")
        }

        data.append(dictionary)

        with open(path, 'w') as jsonFile:
            json.dump(data, jsonFile, indent=3)

        update.message.reply_text(EmojiDictionary[number])
        


def startFunction(update, context):
    update.message.reply_text(messageDictionary["start"])

def helpFunction(update, context):
    update.message.reply_text(messageDictionary["help"])

def brainFunction(update, context):
    user = update.message.from_user
    sendEmoji(user, "brain", update, context)

def smartFunction(update, context):
    user = update.message.from_user
    sendEmoji(user, "smart", update, context)

def codeFunction(update, context):
    user = update.message.from_user
    sendEmoji(user, "code", update, context)

def geekFunction(update, context):
    user = update.message.from_user

    global geek 

    if geek != 1:
        if randint(1,2) == 1:
            sendEmoji(user, "code", update, context)
        else:
            sendEmoji(user, "alien", update, context)
        geek = 1
    else:
        update.message.reply_text("Une seule commande par utilisateur est autorisée par jour")



def alienFunction(update, context):
    user = update.message.from_user
    sendEmoji(user, "alien", update, context)

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