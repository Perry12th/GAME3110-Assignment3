import random 
import socket
import time
import requests
from _thread import *
import threading
from datetime import datetime
import string
import json

def updatePlayerInfo(playerID, newRank):
    # Perform an update reuqest to the database via lambda function
    baseUrl = "https://0qg7o4qjz1.execute-api.us-east-1.amazonaws.com/default/UpdatePlayerInfo?newRank=" + newRank + "&playerID=" + playerID
    #endpoint = "/default/UpdatePlayerInfo"
    #queryParams = {'playerID' : playerID, 'newRank' : newRank}
    requests.get(baseUrl)

def sendPlayersToMatch(sock, gamesToRun):
    print("Sending players to the server")
    playersList = ['001', '012', '013', '017', '022', '035', '045', '010', '107', '666']
    players2Send = random.sample(playersList, gamesToRun * 3)
    print("The following players have entered the lobby: ")
    print(players2Send)
    message = json.dumps(players2Send)
    sock.sendto(bytes(message, 'utf8'), ("127.0.0.1",12345))


def gameLoop(sock):
    #while True:
        # Get match data from the multiplayer server
        print('Waiting for match')
        gameData, addr = sock.recvfrom(1024)
        gameData = json.loads(gameData)
        # gameData = {'id': 670300, 'players': [{'name': 'LynnBoi', 'user_id': '107', 'rank': '1600'}, {'name': 'Travler', 'user_id': '045', 'rank': '1800'}, {'name': 'DawnBringer', 'user_id': '001', 'rank': '1000'}]}
        print(gameData)

        if ('id' in gameData):
            print("A new match has started")
            # Set the match time as the current time
            gameData['matchTime'] = datetime.now()
            # Pick the placement of the players randomly (via shuffle)
            random.shuffle(gameData['players'])
            standing = 1
            for player1 in gameData['players']:
                player1['standing'] = standing
                standing += 1
                player1['timeJoined'] = datetime.now()
                print(player1['name'] + "joined the match!")
            # Update each player's score
            Kfactor = 32
            for player2 in gameData['players']:
                newRank = int(player2['rank'])
                for player3 in gameData['players']:
                    if (player2 != player3):
                        # Figure out the expected score
                        rankA = int(player2['rank'])
                        rankB = int(player3['rank'])
                        expected = 1 / ( 1 + pow(10, int(rankB - rankA / 400)))

                        # Then determine the match score
                        match = 0
                        if (player2['standing'] > player3['standing']):
                            match = 1
                        
                        # Add the rank change to the new rank
                        newRank += int((match - expected) * Kfactor)
                        
                # finally update the player's rank on the database
                updatePlayerInfo(player2['user_id'], str(newRank))
                player2['newRaNK'] = newRank


            # Create the log (file name is the game's id number)
            createLog(gameData)

        #time.sleep(1.0)

def createLog(gameData):
    print('making log')
    fileName = str(gameData['id']) + '.txt'
    with open(fileName, 'w') as f:
        print(gameData, file=f)

def main():
    gamesToRun = random.randint(1,3)
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    start_new_thread(gameLoop, (s,))
    gameLoop(s)
    sendPlayersToMatch(s, gamesToRun)
    while True:
      time.sleep(1.0)

if __name__ == '__main__':
   main()
