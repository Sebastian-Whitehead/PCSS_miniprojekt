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

        self.run()

    def run(self):
        self.s.listen(5)
        while True:
            self.isGameReady()

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
        print('Sending:', message, 'to', player.getName())
        message = json.dumps(message).encode()
        # Packages the message with a matching key
        package = {key: message}
        # Send reply to server
        player.c.send(pickle.dumps(package))

    def request(self, player: Player, message: [str], key: str) -> str:
        print('Requesting:', key)
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
        if self.minPlayers <= len(self.players) and self.host and self.status != 'playing':
            print('Game ready. Request host (' + self.getGameHost().getName() + ') to start')
            if self.request(self.getGameHost(), 'none', 'startGameRequest') == 'True':
                self.startGame()
        return False

    def startGame(self):
        print('START GAME!!')
        self.status = 'playing'
        self.feedback = 0

        # Send image to all players
        for player in self.players:
            self.sendMessage(player, 'Game has started!', 'message')
            self.request(player, self.memeImage.image, 'imageTextRequest')

        #if len(self.players) <= self.feedBack:
            # Request score from players
            #for player in self.players:
              #  self.sendMessage(player, 'Game has started!')
               # self.request(player, [self.memeImage.image], 'imageScoreRequest')

    def makeMeme(self, memeImage: MemeImage, players: Player) -> [MemeImage]:
        pass

    def getScore(self, memeImage: MemeImage, players: Player) -> [int]:
        for player in players:
            self.request(player, 'scoreRequest', 'none')
        pass

    def setGameHost(self, player: Player):
        self.gameHost = player

    def getGameHost(self) -> Player:
        return self.gameHost

    def kill(self):
        self.c.close()
