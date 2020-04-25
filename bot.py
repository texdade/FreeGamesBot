import requests
import json
import csv

class gamesBot():
    def __init__(self):
        self.token = self.readTokenFromFile('bot_config.cfg')
        print(self.token)
        self.link = "https://api.telegram.org/bot{}/".format(self.token)

    def sendMessage(self, msg):
        url = self.link + "sendMessage?chat_id={}&text={}".format('@mockfreesteamstuff', msg)
        if msg is not None:
            print("Sent message [" + msg + "] to " + url)
            requests.get(url)

    def readTokenFromFile(self, config):
        with open('bot_config.cfg') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                return str(row[0])
