from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import os
from dotenv import load_dotenv
from dictionary import messageDictionary, brainEmojiDictionary, codeEmojiDictionary, alienEmojiDictionary, drinkDictionary, drinkEmojiDictionary
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
            "drink" : 0,
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

def drinkFunction(user, text, update, context):

    verifyAccount(user,update)

    newUser = 1

    username = user['username']
    userID = user["id"]
    chat_id = update.message.chat_id

    with open(path, 'r') as jsonFile:
        data = json.load(jsonFile)

    for i in range(len(data[str(chat_id)]["users"][str(userID)])):
        if data[str(chat_id)]["users"][str(userID)][i]["drink"] == 1:
            newUser = 2
            
            if text in data[str(chat_id)]["users"][str(userID)][i]["drinkList"]:
                nb = data[str(chat_id)]["users"][str(userID)][i]["drinkList"][text]
                nb += 1
                data[str(chat_id)]["users"][str(userID)][i]["drinkList"][text] = nb
            else:
                data[str(chat_id)]["users"][str(userID)][i]["drinkList"][text] = 1

            newUser = 0

            break

    if newUser == 1:
        print(f"On group {chat_id} add a new User : {username}, ID : {userID}")
        dictionary = {
            "username": username,
            "text":"",
            "drink": 1,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%m/%d/%y"),
            "drinkList": {
                text: 1
            }
            }

        data[str(chat_id)]["users"][str(userID)].append(dictionary)
        
    with open(path, 'w') as jsonFile:
        json.dump(data, jsonFile, indent=3)

    update.message.reply_text(drinkEmojiDictionary[text])
    update.message.reply_text(drinkDictionary[randint(1,len(drinkDictionary))])

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

def coffeeFunction(update, context):
    user = update.message.from_user
    drinkFunction(user, "coffee", update, context)

def beerFunction(update, context):
    user = update.message.from_user
    drinkFunction(user, "beer", update, context)

def drinkSomethingFunction(update, context):
    user = update.message.from_user
    drinkFunction(user, "other", update, context)


def resumFunction(update, context):
    updater = Updater(TOKEN, use_context=True)
    bot = updater.bot
    GetResum(bot, False)

# Resum function
def GetResum(bot,reset=False):

    with open("data.json", 'r') as jsonFile:
        data = json.load(jsonFile)

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

        if info != []:
            finalText += "\n"

        return finalText
    
    def addDrinkResum(channel, drink):
        m = 0
        info = []
        for user in data[str(channel)]["users"]:
            for k in range(len(data[str(channel)]["users"][str(user)])):
                if data[str(channel)]["users"][str(user)][k]["drink"] == 1 and drink in data[str(channel)]["users"][str(user)][k]["drinkList"]:

                    info.append(f'{data[str(channel)]["users"][str(user)][k]["drinkList"][drink]}-{user}-{drink}-{data[str(channel)]["users"][str(user)][k]["username"]}')
                    m += 1
        info.sort()
        info.reverse()

        print(info)
        n = 0
        finalText = ""

        for l in info:
            print(l)
            n += 1
            finalText = f"{finalText}   {n}. @{l.split('-')[3]} avec {l.split('-')[0]} {drinkEmojiDictionary[drink]}\n"

        finalText += "\n"

        return finalText
        
    for channel in data:
        info = []
        if reset:

            HEURE = os.getenv('HEURE')
            MINUTE = os.getenv('MINUTE')

            finalText = messageDictionary["reset"].replace("TIME", f"{HEURE}:{MINUTE}")
        else:
            finalText = messageDictionary["resum"]

        brain = []
        code = []
        alien = []


        for user in data[str(channel)]["users"]:
            for k in range(len(data[str(channel)]["users"][str(user)])):
                if "number" in data[str(channel)]["users"][str(user)][k]:
                    info.append(f'{data[str(channel)]["users"][str(user)][k]["number"]}-{user}-{data[str(channel)]["users"][str(user)][k]["text"]}-{data[str(channel)]["users"][str(user)][k]["username"]}')

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

        finalText += addDrinkResum(channel, "coffee")
        finalText += addDrinkResum(channel, "other")
        finalText += addDrinkResum(channel, "beer")        

        bot.send_message(chat_id=channel, text=finalText)

    if reset:
        data[channel]["users"] = {}
        with open(path, 'w') as jsonFile:
            json.dump(data, jsonFile, indent=3)


def main():

    print("script started")

    HEURE = os.getenv('HEURE')
    MINUTE = os.getenv('MINUTE')

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

    dp.add_handler(CommandHandler("coffee", coffeeFunction))
    dp.add_handler(CommandHandler("beer", beerFunction))
    dp.add_handler(CommandHandler("drink", drinkSomethingFunction))

    # Run bot
    updater.start_polling()
    isSend = 0

    while True:
        time = datetime.now().time()

        if time.hour == HEURE and time.minute == MINUTE and isSend != 1:
            GetResum(bot, True)
            isSend = 1
        else:
            sleep(29)

        if time.hour == HEURE and time.minute == MINUTE + 2:
            isSend = 0


    # Stop bot with CTRL+C
    updater.idle()

if __name__ == '__main__':
    main()
