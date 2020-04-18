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
    websiteSoup = BeautifulSoup(content, features="html.parser")

    #search for interesting part
    promotions = websiteSoup.find_all('tr', class_='app sub')

    for game in promotions:
        gameSoup = BeautifulSoup(str(game), features="html.parser")

        #find game titles and whether they are free
        arr = gameSoup.find_all('b') 
        title = arr[0].contents[0] #game title is in first <b> tag
        try:
            arr[1].contents #if game's free to keep there's an indication into another <b> tag
            keep = True
        except:
            keep = False

        #find out if game promotion is active
        arr = gameSoup.find_all('td', class_='timeago')
        started = arr[0].contents
        started = str(started[0]).split(" ")
        if(started[2] == "ago"):
            active = True
        else:
            active = False

        if(keep):
            print(title)
            print(active)


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
            














