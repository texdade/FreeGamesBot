from bot import gamesBot
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def addNewGame(newGames):
    #set up webdriver to fetch page
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome-stable"
    chrome_driver_binary = "./chromedriver"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    driver.get("https://steamdb.info/upcoming/free/")
    content = driver.page_source

    #set up soup for webscraping
    soup = BeautifulSoup(content, features="html.parser")

    #search for interesting part
    promotions = soup.find_all('tr', class_='app sub')

    print(promotions)


while True:
    newGames = []
    notifiedGames = []
    addNewGame(newGames)

    if(newGames):
        for items in newGames:
            try:
                msg = forgeBotMsg(items)
            except:
                msg = None
            #if msg is not None:
                #gamesBot.sendMessage()
    
    print("Idling one hour...")
    time.sleep(3600)
            

