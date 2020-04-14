import requests
import json
import configparser as cfg

class gamesBot():
    def __init__(self, config):
        self.token = self.readTokenFromFile(bot_config)
        self.link = "https://api.telegram.org/bot{}/".format(self.token)

    def sendMessage(self, msg, chatId):
        url = self.link + "sendMessage?chat_id={}&text={}".format(chatId, msg)
        if msg is not None:
            requests.get(url)

    def readTokenFromFile(config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.read('token')


