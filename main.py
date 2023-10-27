from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import os
from dotenv import load_dotenv
from dictionary import messageDictionary, EmojiDictionary, drinkDictionary, drinkEmojiDictionary
from random import *
import json
from datetime import *
from time import *
from ManageBotData import ManageBotData

load_dotenv()

TOKEN = os.getenv('TOKEN')

global timeformat
timeformat = "%H:%M"

botData = ManageBotData('data.json')

# verify function
def verifyAccount(user,update):

    userID = user["id"]
    chatID = update.message.chat_id

    data = botData.getData()

    dictionary = {
        "channel_name": "undefined",
        "config_time" : f'{os.getenv("HEURE")}:{os.getenv("MINUTE")}',
        "users": {
        }
    }

    if str(chatID) not in data or len(data) == 0:
        data[str(chatID)] = dictionary

    if str(userID) not in data[str(chatID)]["users"]:
        data[str(chatID)]["users"][str(userID)] = []

    botData.setData(data)

#send function
def sendEmoji(text, update, context):

    user = update.message.from_user
    data = botData.getData()
    number = randint(1,len(EmojiDictionary[text]))

    username = user['username']
    userID = user["id"]
    chatID = update.message.chat_id

    verifyAccount(user, update)

    if botData.isNewUser(update, text):
        update.message.reply_text("Une seule commande par utilisateur est autorisée par jour")

    else:
        print(f"On group {chatID} add a new User : {username}, ID : {userID}")

        dictionary = {
            "username": username,
            "drink" : 0,
            "text": text,
            "number": number,
            "time": datetime.now().strftime("%H:%M:%S")
            }

        data[str(chatID)]["users"][str(userID)].append(dictionary)

        update.message.reply_text(EmojiDictionary[text][number])

    botData.setData(data)

def drinkFunction(text, update, context):

    user = update.message.from_user
    username = user['username']
    userID = user["id"]
    chatID = update.message.chat_id

    verifyAccount(user,update)

    newUser = 1

    data = botData.getData()

    if botData.isNewDrinkUser(update):
        print(f"On group {chatID} add a new User : {username}, ID : {userID}")
        dictionary = {
            "username": username,
            "text": "undefined",
            "drink": 1,
            "time": datetime.now().strftime("%H:%M:%S"),
            "drinkList": {
                text: 1
            }
        }

        data[str(chatID)]["users"][str(userID)].append(dictionary)
        botData.setData(data)
    
    else:
        botData.addDrink(text, update)
        

    update.message.reply_text(drinkEmojiDictionary[text])
    update.message.reply_text(drinkDictionary[randint(1,len(drinkDictionary))])

def startFunction(update, context):
    update.message.reply_text(messageDictionary["start"])

def helpFunction(update, context):
    update.message.reply_text(messageDictionary["help"])

def brainFunction(update, context):
    sendEmoji("brain", update, context)

def codeFunction(update, context):
    sendEmoji("code", update, context)

def alienFunction(update, context):
    sendEmoji("alien", update, context)


def coffeeFunction(update, context):
    drinkFunction("coffee", update, context)

def beerFunction(update, context):
    drinkFunction("beer", update, context)

def whiskyFunction(update, context):
    drinkFunction("whisky", update, context)

def drinkSomethingFunction(update, context):
    drinkFunction("other", update, context)

def resumFunction(update, context):
    GetResum(update.message.chat_id, False)
 
# Resum function
def GetResum(channel, reset=False):

    updater = Updater(TOKEN, use_context=True)
    bot = updater.bot

    def addResum(info):
        n = 0
        finalText = ""

        for l in info:
            text = l.split("-")[2]
            n += 1

            finalText = f"{finalText}   {n}. @{l.split('-')[3]} avec {l.split('-')[0]} {EmojiDictionary[text][1]}\n"

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

        # print(info)
        n = 0
        finalText = ""

        for l in info:
            n += 1
            finalText = f"{finalText}   {n}. @{l.split('-')[3]} avec {l.split('-')[0]} {drinkEmojiDictionary[drink]}\n"

        finalText += "\n"
        return finalText


    data = botData.getData()
    info = []

    time = datetime(2000, 1, 1, int(data[str(channel)][str("config_time")].split(":")[0]), int(data[str(channel)][str("config_time")].split(":")[1])) - timedelta(hours=int(os.getenv("TIME")))

    if reset:
        finalText = messageDictionary["reset"].replace("TIME", str(time.strftime(timeformat)))
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
        if text == "brain":
            brain.append(m)

        if text == "code":
            code.append(m)

        if text == "alien":
            alien.append(m)

    finalText += addResum(brain)
    finalText += addResum(code)
    finalText += addResum(alien)

    finalText += addDrinkResum(channel, "coffee")
    finalText += addDrinkResum(channel, "other")
    finalText += addDrinkResum(channel, "beer")        
    finalText += addDrinkResum(channel, "whisky")

    bot.send_message(chat_id=channel, text=finalText)

    if reset:
        data[channel]["users"] = {}
        botData.setData(data)

def configFunction(update, context):

    data = botData.getData()
    TIME = os.getenv("TIME")

    chat = update.message.chat_id

    newTime = update.message.text.replace("/config ","")

    try:
        validtime = datetime.strptime(newTime, timeformat).strftime(timeformat)
    except ValueError:
        update.message.reply_text(f"Time is not valid. Please use %H:%M format.")

    finalTime = datetime(2023, 10, 25, int(validtime.split(":")[0]), int(validtime.split(":")[1])) + timedelta(hours=int(TIME))
 
    data[str(chat)]["config_time"] = str(finalTime.strftime(timeformat))

    botData.setData(data)

    update.message.reply_text(f"New summary time is now set to: {str(validtime)}")


def main():

    print("script started")

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    bot = updater.bot

    # Base Command
    dp.add_handler(CommandHandler("start", startFunction))
    dp.add_handler(CommandHandler("help", helpFunction))

    dp.add_handler(CommandHandler("resum", resumFunction))
    dp.add_handler(CommandHandler("config", configFunction))

    # Print Command
    dp.add_handler(CommandHandler("brain", brainFunction))
    dp.add_handler(CommandHandler("smart", brainFunction))

    dp.add_handler(CommandHandler("code", codeFunction))
    dp.add_handler(CommandHandler("geek", codeFunction))

    dp.add_handler(CommandHandler("alien", alienFunction))
    dp.add_handler(CommandHandler("ufo", alienFunction))

    dp.add_handler(CommandHandler("coffee", coffeeFunction))
    dp.add_handler(CommandHandler("beer", beerFunction))
    dp.add_handler(CommandHandler("whisky", whiskyFunction))
    dp.add_handler(CommandHandler("drink", drinkSomethingFunction))

    # Run bot
    updater.start_polling()
    isSend = 0

    while True:
        time = datetime.now().time()

        with open("data.json", 'r') as jsonFile:
            data = json.load(jsonFile)

        for channel in data:
            if int(time.hour) == int(data[channel][str("config_time")].split(":")[0]) and int(time.minute) == int(data[channel]["config_time"].split(":")[1]):
                GetResum(channel, True)
                
        sleep(60)

    # Stop bot with CTRL+C
    updater.idle()

if __name__ == '__main__':
    main()
