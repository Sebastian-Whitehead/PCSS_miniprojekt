from MemeImage import MemeImage

class GameEngine():
    def __init__(self):
        self.players = []               # All players that are currently on the server (Keeps on disconnect)
        self.memeImage = MemeImage()    # Meme image (Not implemented)

        self.minPlayers = 1             # Minimum players on the server before the game can start
        self.gameHost = False           # The game host
        self.setStatus('booting')

    def gameRunning(self, server):
        self.isGameReady(server)
        self.imageScoreRequest(server)
        self.handlingScore(server)

    def isGameReady(self, server) -> bool:
        if self.minPlayers <= len(self.players) and self.host and self.status == 'inLobby':
            print('Game ready. Request host (' + self.getGameHost().getName() + ') to start')
            gameStart = self.request(self.getGameHost(), 'none', 'startGameRequest')
            if gameStart == 'True':
                self.startGame(server)
            else:
                self.isGameReady(server)
        return False

    def startGame(self, server):
        print('START GAME!!')
        self.setStatus('imageTextRequest')

        # Send image to all players
        for player in self.players:
            server.sendMessage(player, 'Game has started!', 'message')
            print('')
            server.request(player, self.memeImage.image, 'imageTextRequest')

        print('')

    def imageScoreRequest(self, server):
        if len(self.players) <= self.feedback and self.status == 'imageTextRequest':
            print('All players has send their image text')
            self.setStatus('imageScoreRequest')

            # Request score from players
            for player in self.players:
                server.request(player, [self.memeImage.image], 'imageScoreRequest')

            print('')

    def handlingScore(self, server):
        if len(self.players) <= self.feedback and self.status == 'imageScoreRequest':
            print('All players has send their opinion')
            self.setStatus('handlingScore')

            # Handling score
            print('Handling score..')

            """ CODE MISSING """

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

    def setStatus(self, status: str) -> bool:
        self.status = status
        self.feedback = 0
        return True