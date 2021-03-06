from bot import gamesBot
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

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
        if(keep and started[2] == "ago"):
            active = True

            #if offer's active, check if it's a game and not a dlc/soundtrack
            arr = gameSoup.find_all('a')
            infoUrl = "https://steamdb.info"+arr[1]['href']
            driver.get(infoUrl)
            gameInfo = driver.page_source
            infoSoup = BeautifulSoup(gameInfo, features="html.parser")
            #find all games
            arr = infoSoup.find_all('td', string="Game")
            if(len(arr) > 0):
                isGame = True
            else:
                isGame = False
        else:
            active = False

        #if the promotion is a free to keep game (not dlc or stuff) and also active, 
        # add it to the game to be notified
        if(keep and isGame and active):
            newGames.add(title)

    #close chrome after having checked on all games
    driver.quit()

def forgeBotMsg(title):
    return str(title) + " gratis su Steam"


# # # # # # # # #
#     MAIN      #
# # # # # # # # #

#dictionary containing all the game promotions already notified
notifiedGames = set()

gamesBot = gamesBot()

#csv file containing all the games that have already been sent to the telegram bot
with open('notifiedPromotions.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        notifiedGames.add(str(row[0]))
        

#main loop that repeats every hour
while True:
    newGames = set()
    addNewGame(newGames)
    
    #Remove the notified promotions which are no more active
    removedGames = notifiedGames - newGames
    #Notify only the promotions which weren't notified before
    newGames = newGames - notifiedGames
    notifiedGames = notifiedGames - removedGames
    
    if(newGames):
        for item in newGames:
            try:
                msg = forgeBotMsg(item)
            except:
                msg = None
            if msg is not None:
                gamesBot.sendMessage(msg)
    
    #add the new game to the notified ones
    notifiedGames = notifiedGames.union(newGames)
    
    #update csv file with notified games in case of crash
    with open('notifiedPromotions.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for game in notifiedGames:
            csv_writer.writerow([game])

    print("Idling eight hours...")
    time.sleep(3600*8)
            














