import os, json

class ManageJSONData:
    """class to manage data.json file"""

    def __init__(self, datafile='data.json'):
        self.datafile = datafile
        if not os.path.exists(self.datafile):
            with open(self.datafile, 'w') as f:
                json.dump({}, f)

        with open(self.datafile, 'r') as jsonFile:
            self.data = json.load(jsonFile)
    
    def getDatafile(self):
        return self.datafile

    def getData(self):
        return self.data

    def setData(self, data):
        with open(self.datafile, 'w') as jsonFile:
            json.dump(data, jsonFile, indent=2)


class ManageBotData(ManageJSONData):

    def __init__(self, datafile='data.json'):
        super().__init__(datafile)

    def isNewUser(self, update, text):
        data = self.getData()

        user = update.message.from_user
        userID = user["id"]
        chatID = update.message.chat_id

        for number in range(len(data[str(chatID)]["users"][str(userID)])):
            if data[str(chatID)]["users"][str(userID)][number]["text"] == text:
                return True
            
        return False
    
    def isNewDrinkUser(self, update):
        data = self.getData()

        user = update.message.from_user
        userID = user["id"]
        chatID = update.message.chat_id

        if data[str(chatID)]["users"][str(userID)] == []:
            return True
            
        return False
        
            
    def addDrink(self, drink, update):

        data = self.getData()

        user = update.message.from_user
        userID = user["id"]
        chatID = update.message.chat_id

        for number in range(len(data[str(chatID)]["users"][str(userID)])):
            if data[str(chatID)]["users"][str(userID)][number]["drink"] == 1:
                if drink in data[str(chatID)]["users"][str(userID)][number]["drinkList"]:
                    data[str(chatID)]["users"][str(userID)][number]["drinkList"][drink] += 1
                else:
                   data[str(chatID)]["users"][str(userID)][number]["drinkList"][drink] = 1

        
        self.setData(data)

        

    def getNumberOfUsersOfChannel(self, channelID):
        return len(self.getData()[channelID])

    def hasUserAlreadyUsedCommandX(self, channelID, userID, commandX):
        return True



