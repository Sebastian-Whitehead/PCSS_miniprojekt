import threading
from MemeImage import MemeImage
from Bubble_sort import *
import multiprocessing, ctypes

"""
# Game engine for the game, keeping track of each step
# Will continue to next step of the game, when Feedback
  is equal to amount of players in the game
"""
feedback = 0
points_lock = multiprocessing.Lock()
feedback_lock = multiprocessing.Lock()


class GameEngine():
    def __init__(self):
        # multiprocessing.Process.__init__(self)
        # All players that are currently on the server (Keeps on disconnect)
        self.players = []
        # Meme image (Not implemented)
        self.memeImage = MemeImage()
        # Text from all players
        self.texts = []
        # Points given from all players
        self.points = []

        # Minimum players on the server before the game can start
        self.minPlayers = 1
        # The game host
        self.gameHost = False
        # Set state of program
        self.setStatus('booting')

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
            gameStart = self.request(self.getGameHost(), 'none', 'startGameRequest')
            if gameStart == 'True':
                # Start the game
                self.startGame(server)
            else:
                # Keep listening for host
                self.isGameReady(server)
        return False

    def sendListen(self, server, player, feedback, answer, message, key, pos):
        server.sendMessage(player, message, key)  # Send message to server
        value = server.listen(player, key)
        if value.isdigit():
            value = int(value)
        # else: value = value.encode('utf-8')

        print(f'{value=}')
        print(f"{ctypes.c_wchar_p(value)=}")
        answer[pos] = ctypes.c_wchar_p(value)  # Input value into
        print(f"{answer=}")
        print(f"{answer[pos]=}")

        # TODO: ADD WAITING FOR OTHER PLAYERS SCREEN HERE
        # Add feedback to continue
        feedback.value += 1
        print("feedback updated")

    def startThread(self, server, type, message, key):
        print("\nSTARTING THREAD")
        returnedData = []
        t = {}  # Dictionary of active threads
        FB = multiprocessing.Value('i', 0)  # Process safe feedback varriable
        ans = multiprocessing.Array(type, len(self.players))  # Process safe response variable

        # Request score from players
        for pos, player in enumerate(self.players):
            print(f"{pos=}")
            # start a thread for each player that requests score and listens for an answer
            t[pos] = multiprocessing.Process(
                target=self.sendListen,
                args=(server, player, FB, ans, message, key, pos)
            )
            t[pos].start()
            print(f"{t=}")

        for pos in t:  # After all threads are started begin to join the threads 1 by one
            print(f"JOINING THREAD{pos}")
            t[pos].join()  # Wait for thread to complete then join
            print("THREAD JOINED")
            self.feedback += FB.value  # transfer the variables to the corresponding local definitions.

            print(f"{ans=}")
            print(f"{pos=}")
            print(f"{ans[pos]=}")
            returnedData.append(ctypes.c_wchar_p(ans))

        print(f"{returnedData=}")

        return returnedData

    # Start the game - send random image to all players
    # Get meme or image text in return
    def startGame(self, server):
        print('START GAME!!')
        self.setStatus('imageTextRequest')

        # Send image to all players
        self.texts = self.startThread(server, ctypes.c_wchar_p, self.memeImage.getImageName(), 'imageTextRequest')
        print("I STARTED THE GAME!!!")
        print(f'{self.points}', end='\n\n')

    # Send all memes to all players
    # Request each player for a favorite meme
    def imageScoreRequest(self, server):
        if len(self.players) <= self.feedback and self.status == 'imageTextRequest':
            print('All players has send their image text')
            self.setStatus('imageScoreRequest')

            self.points = self.startThread(server, 'i', self.texts, 'imageScoreRequest')
            print("WTF")
            print(f'{self.points}', end='\n\n')

    # Handle favorite memes and calculate a score
    # Send message to all player who the winner is, and what image it is
    def handlingScore(self, server):
        print(f"nr of player= {len(self.players)}, feedback = {self.feedback}, {self.status}")
        if len(self.players) <= self.feedback and self.status == 'imageScoreRequest':
            print('All players has send their opinion')
            self.setStatus('handlingScore')

            # Handling score
            print('Handling score..')
            print('All points:', self.points)
            countedPoints = countPoints(self.points, len(self.players))
            print('CountedPoints:', countedPoints)
            sortedPoints = bubble_sort(countedPoints)
            print('sortedPoints:', sortedPoints)
            winnerValue = max(countedPoints)
            winnerIndex = countedPoints.index(winnerValue)
            winner = 'Player ' + str(winnerIndex)
            print('Winner is', winner)
            print('')

            # Sending winner to all players
            for player in self.players:
                server.sendMessage(player, winner, 'winnerChickenDinner')
            print('')

            # Request new game
            print('Requesting new game..')
            print('')
            self.memeImage.newRandomImage()
            self.setStatus('inLobby')
            return server.run()

    # Set the status and reset feedback
    # Feedback will activate the next step of the game,
    # when all players has reacted in the current step
    def setStatus(self, status: str) -> bool:
        self.status = status
        self.feedback = 0
        return True


if __name__ == '__main__':
    GameEngine()
