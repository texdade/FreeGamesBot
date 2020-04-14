from bot import gamesBot

while True:
    print("Idle...")

    newGames = None #modificare dopo plz

    if(newGames):
        for items in newGames:
            try:
                msg = forgeBotMsg(items)
            except:
                msg = None
            if msg is not None:
                bot.sendMessage()
            

