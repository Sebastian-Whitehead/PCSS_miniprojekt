class GameEngine:
    def __init__(self):
        self.status = 'booting'
        self.minPlayers = 1     # Minimum players on the server before the game can start
        self.gameHost = False   # The game host
        self.feedback = 0       # How many have gaven feedback to the server

    def gameRunning(self):
        self.isGameReady()
        self.imageScoreRequest()
        self.handlingScore()

    def isGameReady(self) -> bool:
        if self.minPlayers <= len(self.players) and self.host and self.status == 'inLobby':
            print('Game ready. Request host (' + self.getGameHost().getName() + ') to start')
            gameStart = self.request(self.getGameHost(), 'none', 'startGameRequest')
            if gameStart == 'True':
                self.startGame()
            else:
                self.isGameReady()
        return False

    def startGame(self):
        print('START GAME!!')
        self.status = 'imageTextRequest'
        self.feedback = 0

        # Send image to all players
        for player in self.players:
            self.sendMessage(player, 'Game has started!', 'message')
            print('')
            self.request(player, self.memeImage.image, 'imageTextRequest')

        print('')

    def imageScoreRequest(self):
        if len(self.players) <= self.feedback and self.status == 'imageTextRequest':
            print('All players has send their image text')
            self.status = 'imageScoreRequest'
            self.feedback = 0

            # Request score from players
            for player in self.players:
                self.request(player, [self.memeImage.image], 'imageScoreRequest')

            print('')

    def handlingScore(self):
        if len(self.players) <= self.feedback and self.status == 'imageScoreRequest':
            print('All players has send their opinion')
            self.status = 'handlingScore'
            self.feedback = 0

            print('Handling score..')
            winner = "'pass'"
            print('')

            # Sending winner to all players
            for player in self.players:
                self.sendMessage(player, 'Winner is ' + winner + '!', 'message')
            print('')

            print('Requesting new game')
            print('')
            self.memeImage.newRandomImage()
            self.status = 'inLobby'
            self.run()