import numpy as np

from MemeImage import MemeImage
import Bubble_sort, handleHighScoreList
import threading as th
from Player import Player

"""
# Game engine for the game, keeping track of each step
# Will continue to next step of the game, when Feedback
  is equal to amount of players in the game
"""


class GameEngine():
    def __init__(self):
        # multiprocessing.Process.__init__(self)
        self.players = []  # All players that are currently on the server (Keeps on disconnect)
        self.memeImage = MemeImage()  # Meme image (Not implemented)
        self.texts = []  # Text from all players
        self.points = []  # Points given from all players
        self.minPlayers = 1  # Minimum players on the server before the game can start
        self.gameHost = False  # The game host
        self.setStatus('booting')  # Set state of program

    # Run the Game Engine on the server
    def gameRunning(self, server):
        print('Game running..')
        self.isGameReady(server)
        self.imageScoreRequest(server)
        self.handlingScore(server)

    # Sending game start request to game host, when game is ready to start
    def isGameReady(self, server) -> bool:
        if self.minPlayers <= len(self.players) and self.host and self.status == 'inLobby':
            print('Game ready. Request host (' + self.getGameHost().getName() + ') to start')
            gameStart = self.request(self.getGameHost(), 'Request game to start', 'startGameRequest')
            print(f'{gameStart=}')
            if gameStart == 'True':  self.startGame(server)  # Start the game
            print('Waiting to start')

    def sendListen(self, server, player, answer, message, key):
        print(f">>>>>>> {player =}, {message =}, {key =}")
        server.sendMessage(player, message, key)  # Send message to server
        value = server.listen(player, key)

        # if value.isdigit(): value = int(value)
        if key == 'imageScoreRequest':
            answer[int(value)] += 1

        elif key == 'imageTextRequest':
            answer[int(player.ID)] = f"{player.ID}:{value}"

        # Add feedback to continue
        self.feedback += 1

    def startThread(self, server, message, key):
        print("=============== STARTING THREAD =================")
        returnedData = []
        t = {}
        if key == 'imageTextRequest':
            ans = ['' for x in range(len(self.players))]
        else:
            ans = [0] * len(self.players)

        # Request score from players
        for pos, player in enumerate(self.players):
            # start a thread for each player that requests score and listens for an answer
            t[pos] = th.Thread(
                target=self.sendListen,
                args=(server, player, ans, message, key)
            )
            t[pos].start()

        for pos in t:  # After all threads are started begin to join the threads 1 by one
            t[pos].join()  # Wait for thread to complete then join
            print(f'{ans[:]}, {type(ans)=}')

        # self.feedback += FB  # transfer the variables to the corresponding local definitions.

        returnedData.extend(ans)
        # print(f'{self.feedback=}, {self.points=}, {FB=}')
        # print(f'{ans[:]=}, {self.points=}, {FB=}')

        return returnedData

    # Start the game - send random image to all players
    # Get meme or image text in return
    def startGame(self, server):
        print('START GAME!!')
        self.setStatus('imageTextRequest')

        print(f'\n')
        print("============ REQUESTING PLAYER TEXTS ===========")

        self.texts = self.startThread(
            server=server,
            message=self.memeImage.getImageName(),
            key='imageTextRequest'
        )
        print(f"{self.texts=}")
        print('')

    # Send all memes to all players
    # Request each player for a favorite meme
    def imageScoreRequest(self, server):
        if len(self.players) <= self.feedback and self.status == 'imageTextRequest':
            print("=========== REQUESTING SCORE =============")
            print('All players has send their image text')
            self.setStatus('imageScoreRequest')

            """ # Manufactured data (start) #
            self.texts = ['0:Test0', '1:awdawd', '2:awddddd', '3:dddddd']
            print(f'{self.texts=}')
            # Manufactured data (end) # 
            """

            self.points = self.startThread(
                server=server,
                message=self.texts,
                key='imageScoreRequest'
            )
            print(f'{self.points=}', end='\n\n')

    # Handle favorite memes and calculate a score
    # Send message to all player who the winner is, and what image it is
    def handlingScore(self, server):

        if len(self.players) <= self.feedback and self.status == 'imageScoreRequest':
            print("=========== HANDELING SCORE =============")
            print(f"nr of player= {len(self.players)}, feedback = {self.feedback}, {self.status}")
            self.setStatus('handlingScore')

            # Count points
            print('Handling score..')
            print('All points:', self.points)

            # countedPoints = Bubble_sort.countPoints(self.points)
            # print(f'{countedPoints=}')

            # Zip score with name
            playerNames = [player.name for player in self.players]
            # playerNames = [player.name for player in self.players]
            packedScores = list(zip(playerNames, self.points))
            print(f'{packedScores=}')

            # Save to all time high score list
            handleHighScoreList.saveScores('allTimeHighScore.txt', packedScores)

            # Sort scores
            sortedPoints = Bubble_sort.bubble_sort(packedScores)
            print(f'{sortedPoints=}')

            # Sending winner to all players
            for player in self.players:
                server.sendMessage(player, sortedPoints, 'packedScores')
                # server.sendMessage(player, sortedPoints, 'sortedPoints')
            print('')

            # Request new game
            print('Requesting new game..')
            print('')
            self.memeImage.newRandomImage()
            self.setStatus('inLobby')
            # return server.run()

    # Set the status and reset feedback
    # Feedback will activate the next step of the game,
    # when all players has reacted in the current step
    def setStatus(self, status: str) -> bool:
        self.status = status
        self.feedback = 0
        return True


if __name__ == '__main__':
    GameEngine()
