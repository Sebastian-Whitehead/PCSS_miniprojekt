# https://www.tutorialspoint.com/python/python_networking.htm
import json
import socket, pickle
from MemeImage import MemeImage
from Player import Player

"""
To do:
- Send and recive images - Sebastian
- Multi-threading - Tonko
"""

class Server:
    def __init__(self, port):
        self.status = 'booting'
        self.minPlayers = 1          # Minimum players on the server before the game can start
        self.gameHost = False        # The game host
        self.players = []            # All players that are currently on the server (Keeps on disconnect)
        self.feedback = 0            # How many have gaven feedback to the server
        self.memeImage = MemeImage() # Meme image (Not implemented)

        self.s = socket.socket()
        self.host = socket.gethostname()
        self.port = port
        self.s.bind((self.host, self.port))
        print(self.s, 'Server is Running..')
        print('')

        self.status = 'inLobby'
        self.run()

    def run(self):
        self.s.listen(5)
        while True:
            self.isGameReady()
            self.imageScoreRequest()
            self.handlingScore()

            # Server listens for players joining the server
            player = Player()
            player.c, player.addr = self.s.accept()
            print('Got connection from:', player.addr)
            self.sendMessage(player, 'Thank you for connecting.', 'message')
            self.clientJoined(player)

    def clientJoined(self, newPlayer):
        # Check if the user is already connected
        for player in self.players:
            if newPlayer.addr == player.addr:
                return print('Old player')

        # Request the name of the player
        name = self.request(newPlayer, 'none', 'nameRequest')
        newPlayer.setName(name)
        self.players.append(newPlayer)
        print('New player')

        # Confirm player with a message
        message = 'Hi, ' + newPlayer.getName() + '!'
        self.sendMessage(newPlayer, message, 'message')

        # Set player to be game host if none
        if not self.getGameHost():
            self.setGameHost(newPlayer)
            print('Host:', newPlayer.getName())

        print('')

    def sendMessage(self, player: Player, message: [str], key: str):
        # Send message to player
        if message == 'none':
            message = key
        print('Sending:', message, 'to', player.getName())
        message = json.dumps(message).encode()
        # Packages the message with a matching key
        package = {key: message}
        # Send reply to server
        player.c.send(pickle.dumps(package))

    def request(self, player: Player, message: [str], key: str) -> str:
        self.sendMessage(player, message, key)

        # Listen for reply
        self.s.listen(5)
        print('Listening..')
        while True:
            # Getting a reply from the player
            recive = player.c.recv(1024)
            if recive:
                package = pickle.loads(recive)
                clientMessage = package[key].decode()
                print(player.getName(), 'sent:', key, '->', clientMessage)
                self.feedback += 1
                return clientMessage

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

    def setGameHost(self, player: Player):
        self.gameHost = player

    def getGameHost(self) -> Player:
        return self.gameHost

    def kill(self):
        self.c.close()
