from telegram.ext import Updater, CommandHandler
import os
from dotenv import load_dotenv
from dictionary import messageDictionary, brainEmojiDictionary, codeEmojiDictionary, alienEmojiDictionary
from random import *
import json
from datetime import datetime
import schedule
from time import *

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
    chat_id = update.message.chat_id

    with open(path, 'r') as jsonFile:
        data = json.load(jsonFile)

    for i in range(len(data)):
        if data[i]["id"] == userID:
            if data[i]["chat_id"] == chat_id:
                if data[i]["text"] == text1 or data[i]["text"] == text2:
                    update.message.reply_text("Une seule commande par utilisateur est autorisée par jour")
                    newUser = 0

    if newUser == 1:
        print(f"new User : {username} ")
        dictionary = {
            "chat_id": chat_id,
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

def GetResum(bot):

    chatIDList = []
    userList = []
    newUserList = []
    newUserListNB = []

    userNumber = ""
    finalText = ""
    n = 0

    with open("data.json", 'r') as jsonFile:
        data = json.load(jsonFile)

    for chatID in range(len(data)):

        if data[chatID]["chat_id"] not in chatIDList:
            chatIDList.append(data[chatID]["chat_id"])

    for k in range(3):
        if k == 0:
            EmojiDictionary = brainEmojiDictionary
            text1 = "brain"
            text2 = "smart"
        if k == 1:
            EmojiDictionary = codeEmojiDictionary
            text1 = "code"
            text2 = "geek"
        if k == 2:
            EmojiDictionary = alienEmojiDictionary
            text1 = "geek"
            text2 = "alien"

        for i in range(len(chatIDList)):

            for j in range(len(data)):

                if data[j]["chat_id"] == chatIDList[i]:
                    if data[j]["text"] == text1 or data[j]["text"] == text2:
                        userList.append(data[j]["username"])
                        userNumber = f'{data[j]["number"]}-{data[j]["id"]}-{data[j]["username"]}'
                        newUserList.append(userNumber)

            newUserList.sort()
            newUserList.reverse()
            if userList != "":
                finalText = "Il est 18 heures voici le classement: \n"
                for l in newUserList:
                    print(l)
                    n += 1
                    finalText = finalText+"    "
                    finalText = f"{finalText}{n}. @{l.split('-')[2]} avec {l.split('-')[0]} {EmojiDictionary[1]}"

                    newUserListNB.append(l.split("-")[0])

                    finalText = f"{finalText}\n"
            else:
                print("presonne n'a participé")

            bot.send_message(chat_id=chatIDList[i], text=finalText)

            userList = []
            newUserList = []
            newUserListNB = []
            n = 0

def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    bot = updater.bot

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

    dp.add_handler(CommandHandler("getresume", GetResum))

    # Run bot
    updater.start_polling()
    isSend = 0

    while True:
        time = datetime.now().time()

        if time.hour == 10 and time.minute == 58 and isSend != 1:
            GetResum(bot)
            isSend = 1
        else:
            sleep(10)

    # Stop bot with CTRL+C
    updater.idle()


if __name__ == '__main__':
    main()
