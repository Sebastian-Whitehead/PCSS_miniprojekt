import threading
from MemeImage import MemeImage

"""
# Game engine for the game, keeping track of each step
# Will continue to next step of the game, when Feedback
  is equal to amount of players in the game
"""
class GameEngine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
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

    # Start the game - send random image to all players
    # Get meme or image text in return
    def startGame(self, server):
        print('START GAME!!')
        self.setStatus('imageTextRequest')

        # Send image to all players
        for player in self.players:
            # Request each player
            server.sendMessage(player, 'imageTextRequest', 'message')
            # Append the text to the list
            self.texts.append(player.ID + ':' + server.listen(player, 'imageTextRequest'))
            # Add feedback
            self.feedback += 1
        print('')

    # Send all memes to all players
    # Request each player for a favorite meme
    def imageScoreRequest(self, server):
        if len(self.players) <= self.feedback and self.status == 'imageTextRequest':
            print('All players has send their image text')
            self.setStatus('imageScoreRequest')

            # Request score from players
            for pos, player in enumerate(self.players):
                # Request all players for a score
                server.sendMessage(player, self.texts, 'imageScoreRequest')
                # Append the score to list
                self.points.append(server.listen(player, 'imageScoreRequest'))
                # Add feedback to continue
                self.feedback += 1
            print('')

    # Handle favorite memes and calculate a score
    # Send message to all player who the winner is, and what image it is
    def handlingScore(self, server):
        if len(self.players) <= self.feedback and self.status == 'imageScoreRequest':
            print('All players has send their opinion')
            self.setStatus('handlingScore')

            # Handling score
            print('Handling score..')
            """ CODE MISSING """
            """   CHARLOTTE  """
            winner = "'pass'"
            print('')

            # Sending winner to all players
            for player in self.players:
                server.sendMessage(player, 'Winner is ' + winner + '!', 'message')
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