import socket
import requests
import time
from _thread import *
import threading
import random
import string
import json

matchSize = 3

def getPlayerInfo(playerID):
    # Perform an update reuqest to the database via lambda function
    baseUrl = "https://54wuhluffa.execute-api.us-east-1.amazonaws.com/default/GetPlayerInfo?playerID=" + playerID
    resp = requests.get(baseUrl)
    return json.loads(resp.content)

def connectionLoop(sock):
   # while True:
        # Get the player List from the sim script
        print("Waiting for players")
        LobbyList, addr = sock.recvfrom(1024)
        print("Got something")
        LobbyList = json.loads(LobbyList)
        #LobbyList = ['107', '045', '001', '022', '666', '013']
        print(LobbyList)

        # If there's enough players to make a lobby
        if (len(LobbyList) >= matchSize):
            print("Players have joined!!")
            playerList = []
            # Grab the info for each of the players that is in the lobby
            for player in LobbyList :
                playerList.append(getPlayerInfo(player))
            # Divide the players into groups based on the matchSize
            for match in range(1, int(len(playerList)/matchSize)):
                # grab the first player on the list
                player1 = playerList.pop(0)
                bMnum = 0
                p1 = 0
                p2 = 0
                nbMnum = 0
                # determine the best matches for the first player (2 other players)
                for i in range(len(playerList)):
                    playerMatch = abs(int(player1['rank']) - int(playerList[i]['rank']))
                    if (playerMatch < bMnum):
                        p1 = i
                        bMnum = playerMatch
                    elif (playerMatch < nbMnum):
                        p2 = i
                        nbMnum = playerMatch
                # remove the two other players from the list
                player2 = playerList.pop(p1)
                player3 = playerList.pop(p2)
                # Create the Game match dic with its random id for each group
                gameData = {}
                gameData['id'] = random.randint(0, 1000000)
                gameData['players'] = [player1, player2, player3]
                # Send each gameMatch back to the sim script
                print('Sending the following game data back to the sim script')
                print(gameData)
                message = json.dumps(gameData)
                sock.sendto(bytes(message, 'utf8'), addr)
                
        time.sleep(1.0)


def main():
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    start_new_thread(connectionLoop, (s,))
    while True:
      time.sleep(1.0)

if __name__ == '__main__':
   main()