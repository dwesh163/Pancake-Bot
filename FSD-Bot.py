from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import os
from dotenv import load_dotenv
from dictionary import messageDictionary, brainEmojiDictionary, codeEmojiDictionary, alienEmojiDictionary
from random import *
import json
from datetime import datetime
from time import *

load_dotenv()

TOKEN = os.getenv('TOKEN')

global geek
geek = 0
global path
path = "data.json"

if not os.path.exists(path):
    with open(path, 'w') as f:
        json.dump({}, f)

# verify function
def verifyAccount(user,update):

    username = user['username']
    userID = user["id"]
    chat_id = update.message.chat_id

    with open(path, 'r') as jsonFile:
        data = json.load(jsonFile)

    dictionary = {
        "channel_name": "undefined",
        "users": {
        }
    }

    if str(chat_id) not in data:
        data[chat_id] = dictionary

    if len(data) == 0:
        data[chat_id] = dictionary

    with open(path, 'w') as jsonFile:
        json.dump(data, jsonFile, indent=3)

    sleep(0.1)

    with open(path, 'r') as jsonFile:
        data = json.load(jsonFile)

    dictionary = {
        userID : [

            ]
    }

    if str(userID) not in data[str(chat_id)]["users"]:
        data[str(chat_id)]["users"][userID] = []

    with open(path, 'w') as jsonFile:
        json.dump(data, jsonFile, indent=3)

#send function
def sendEmoji(user, text, update, context):

    verifyAccount(user,update)

    newUser = 1
    
    if text == "brain" or text == "smart":
        text1 = "brain"
        text2 = "smart"
        EmojiDictionary = brainEmojiDictionary
        number = randint(1,len(brainEmojiDictionary))

    if text == "code" or text == "geek":
        text1 = "code"
        text2 = "geek"
        EmojiDictionary = codeEmojiDictionary
        number = randint(1,len(codeEmojiDictionary))

    if text == "ufo" or text == "alien":
        text1 = "ufo"
        text2 = "alien"
        EmojiDictionary = alienEmojiDictionary
        number = randint(1,len(alienEmojiDictionary))

    username = user['username']
    userID = user["id"]
    chat_id = update.message.chat_id

    with open(path, 'r') as jsonFile:
        data = json.load(jsonFile)

    for i in range(len(data[str(chat_id)]["users"][str(userID)])):
        if data[str(chat_id)]["users"][str(userID)][i]["text"] == text1 or data[str(chat_id)]["users"][str(userID)][i]["text"] == text2:
            update.message.reply_text("Une seule commande par utilisateur est autorisée par jour")
            newUser = 0

    if newUser == 1:
        print(f"On group {chat_id} add a new User : {username}, ID : {userID}")
        dictionary = {
            "username": username,
            "text": text,
            "number": number,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%m/%d/%y"),
            }

        data[str(chat_id)]["users"][str(userID)].append(dictionary)

        with open(path, 'w') as jsonFile:
            json.dump(data, jsonFile, indent=3)

        update.message.reply_text(EmojiDictionary[number])
        Isgeek = 0

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
    sendEmoji(user, "geek", update, context)

def ufoFunction(update, context):
    user = update.message.from_user
    sendEmoji(user, "ufo", update, context)

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

def resumFunction(update, context):
    updater = Updater(TOKEN, use_context=True)
    bot = updater.bot
    GetResum(bot)

# Resum function
def GetResum(bot):

    with open("data.json", 'r') as jsonFile:
        data = json.load(jsonFile)

    for i in data:
        info = []
        finalText = "Il est 18 heures voici le classement: \n\n"

        brain = []
        code = []
        alien = []

        def addResum(info):
            n = 0
            finalText = ""

            for l in info:
                text = l.split("-")[2]
                if text == "brain" or text == "smart":
                    EmojiDictionary = brainEmojiDictionary

                if text == "code" or text == "geek":
                    EmojiDictionary = codeEmojiDictionary

                if text == "ufo" or text == "alien":
                    EmojiDictionary = alienEmojiDictionary

                n += 1
                finalText = f"{finalText}   {n}. @{l.split('-')[3]} avec {l.split('-')[0]} {EmojiDictionary[1]}\n"

            finalText += "\n"

            return finalText

        for j in data[str(i)]["users"]:
            for k in range(len(data[str(i)]["users"][str(j)])):
                info.append(f'{data[str(i)]["users"][str(j)][k]["number"]}-{j}-{data[str(i)]["users"][str(j)][k]["text"]}-{data[str(i)]["users"][str(j)][k]["username"]}')

        info.sort()
        info.reverse()

        for m in info:
            text = m.split("-")[2]
            if text == "brain" or text == "smart":
                brain.append(m)
                EmojiDictionary = brainEmojiDictionary

            if text == "code" or text == "geek":
                EmojiDictionary = codeEmojiDictionary
                code.append(m)

            if text == "ufo" or text == "alien":
                EmojiDictionary = alienEmojiDictionary
                alien.append(m)

        finalText += addResum(brain)
        finalText += addResum(code)
        finalText += addResum(alien)

        bot.send_message(chat_id=i, text=finalText)

    with open("data.json", 'r') as jsonFile:
        data = json.load(jsonFile)

    data = {}

    with open(path, 'w') as jsonFile:
        json.dump(data, jsonFile, indent=3)  


 
def main():

    print("script started")

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    bot = updater.bot

    # Base Command
    dp.add_handler(CommandHandler("start", startFunction))
    dp.add_handler(CommandHandler("help", helpFunction))

    # Print Command
    dp.add_handler(CommandHandler("brain", brainFunction))
    dp.add_handler(CommandHandler("smart", smartFunction))

    dp.add_handler(CommandHandler("resum", resumFunction))

    dp.add_handler(CommandHandler("code", codeFunction))
    dp.add_handler(CommandHandler("geek", geekFunction))

    dp.add_handler(CommandHandler("alien", alienFunction))
    dp.add_handler(CommandHandler("ufo", ufoFunction))

    dp.add_handler(CommandHandler("drink", drinkFunction))
    dp.add_handler(CommandHandler("coffee", coffeeFunction))
    dp.add_handler(CommandHandler("beer", beerFunction))
    dp.add_handler(CommandHandler("drink_something", drinkSomethingFunction))

    dp.add_handler(CommandHandler("getresume", GetResum))

    # Run bot
    updater.start_polling()
    isSend = 0

    while True:
        time = datetime.now().time()

        if time.hour == 18 and time.minute == 0 and isSend != 1:
            GetResum(bot)
            isSend = 1
        else:
            sleep(10)

        if time.hour == 18 and time.minute == 4:
            isSend = 0


    # Stop bot with CTRL+C
    updater.idle()


if __name__ == '__main__':
    main()
