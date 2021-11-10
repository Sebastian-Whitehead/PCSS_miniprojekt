from MemeImage import MemeImage
import Bubble_sort, handleHighScoreList
import multiprocessing, ctypes, json, random
from Player import Player

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

    def sendListen(self, server, player, feedback, answer, message, key):
        server.sendMessage(player, message, key)  # Send message to server
        value = server.listen(player, key)
        if value.isdigit(): value = int(value)
        #else: value = value.encode('utf-8')
        print(f'{player.ID=}')
        print(f'{value=}, {type(value)=}')
        print(f'{answer[:]=}')
        answer[int(player.ID)] = value  # Append the score to list
        player.answer = value
        print(f'{answer[:]=}')

        # TODO: ADD WAITING FOR OTHER PLAYERS SCREEN HERE
        # Add feedback to continue
        feedback.value += 1

    def startThread(self, server, type, message, key):
        returnedData = []
        t = {}
        FB = multiprocessing.Value('i', 0)
        ans = multiprocessing.Array('i', range(len(self.players)))

        # Request score from players
        for pos, player in enumerate(self.players):
            # start a thread for each player that requests score and listens for an answer
            t[pos] = multiprocessing.Process(
                target=self.sendListen,
                args=(server, player, FB, ans, message, key)
            )
            t[pos].start()

        for pos in t:  # After all threads are started begin to join the threads 1 by one
            t[pos].join()  # Wait for thread to complete then join
        self.feedback = FB.value  # transfer the variables to the corresponding local definitions.
        returnedData.extend(ans)

        print(f'{self.feedback=}, {self.points=}, {FB.value=}')
        print(f'{ans[:]=}, {self.points=}, {FB.value=}')

        return returnedData

    # Start the game - send random image to all players
    # Get meme or image text in return
    def startGame(self, server):
        print('START GAME!!')
        self.setStatus('imageTextRequest')

        # Send image to all players
        for player in self.players:
            # Request each player
            print()
            server.sendMessage(player, self.memeImage.getImageName(), 'imageTextRequest')
            # Append the text to the list
            self.texts.append(player.ID + ':' + server.listen(player, 'imageTextRequest'))
            # Add feedback
            self.feedback += 1
        print('')

        """
        # Send image to all players
        self.texts = self.startThread(server, ctypes.c_char_p, self.memeImage.getImageName(), 'imageTextRequest')
        print(f'{self.points}', end='\n\n')
        """

    # Send all memes to all players
    # Request each player for a favorite meme
    def imageScoreRequest(self, server):
        if len(self.players) <= self.feedback and self.status == 'imageTextRequest':
            print('All players has send their image text')
            self.setStatus('imageScoreRequest')

            """ # Manufactured data (start) #
            self.texts = ['0:Test0', '1:awdawd', '2:awddddd', '3:dddddd']
            print(f'{self.texts=}')
            # Manufactured data (end) # 
            """

            self.points = self.startThread(server, 'i', self.texts, 'imageScoreRequest')
            print(f'{self.points}', end='\n\n')

    # Handle favorite memes and calculate a score
    # Send message to all player who the winner is, and what image it is
    def handlingScore(self, server):
        print(f"nr of player= {len(self.players)}, feedback = {self.feedback}, {self.status}")
        if len(self.players) <= self.feedback and self.status == 'imageScoreRequest':
            print('All players has send their opinion')
            self.setStatus('handlingScore')

            """ # Manufactured data (start) # 
            self.manuPlayers = [Player(), Player(), Player(), Player()]
            self.manupoints = []
            for i in range(50):
                n = random.randint(0, len(self.manuPlayers))
                self.manupoints.append(n)

            self.points = self.manupoints
            print(f'{self.points=}')
            print(f'{self.manuPlayers=}')
            # Manufactured data (end) # 
            """

            # Count points
            print('Handling score..')
            print('All points:', self.points)
            countedPoints = Bubble_sort.countPoints(self.points)
            print(f'{countedPoints=}')

            # Zip score with name
            playerNames = [player.name for player in self.manuPlayers]
            # playerNames = [player.name for player in self.players]
            packedScores = list(zip(playerNames, countedPoints))
            print(f'{packedScores=}')

            # Save to all time high score list
            handleHighScoreList.saveScores('allTimeHighScore.txt', packedScores)

            # Sort scores
            sortedPoints = Bubble_sort.bubble_sort(packedScores)
            print(f'{sortedPoints=}')

            """
            sortedNames = [player[0] for player in sortedPoints]
            print(f'{sortedNames=}')
            sortedPoints = [player[1] for player in sortedPoints]
            print(f'{sortedPoints=}')
            """

            # Sending winner to all players
            for player in self.players:
                server.sendMessage(player, sortedPoints, 'packedScores')
                #server.sendMessage(player, sortedPoints, 'sortedPoints')
            print('')

            # Request new game
            print('Requesting new game..')
            print('')
            self.memeImage.newRandomImage()
            self.setStatus('inLobby')
            #return server.run()

    # Set the status and reset feedback
    # Feedback will activate the next step of the game,
    # when all players has reacted in the current step
    def setStatus(self, status: str) -> bool:
        self.status = status
        self.feedback = 0
        return True


if __name__ == '__main__':
    GameEngine()
