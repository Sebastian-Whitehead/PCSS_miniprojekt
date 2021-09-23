# https://www.tutorialspoint.com/python/python_networking.htm
import socket, pickle
from MemeImage import MemeImage
from Player import Player

"""
To do:
- Send and recive images - Tonko
- Multi-threading - Seb
"""

class Server:
    def __init__(self, port):
        self.status = 'booting'
        self.minPlayers = 1          # Minimum players on the server before the game can start
        self.gameHost = False        # The game host
        self.players = []            # All players that are currently on the server (Keeps on disconnect)
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
            self.sendMessage(player, 'Thank you for connecting.')
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
        message = 'Hi, ' + newPlayer.name + '!'
        self.sendMessage(newPlayer, message)

        # Set player to be game host if none
        if not self.gameHost:
            self.setGameHost(newPlayer)
            print('Host:', newPlayer.name)

        print('')

    def sendMessage(self, player: Player, message: str):
        # Send request message to player
        print('Sending:', message, 'to', player.name)
        message = message.encode()
        # Packages the message with a matching key
        package = {'none': message}
        # Send reply to server
        player.c.send(pickle.dumps(package))

    def request(self, player: Player, message: str, key: str) -> str:
        # Send request message to player
        print('Requesting:', key)
        message = message.encode()
        # Packages the message with a matching key
        package = {key: message}
        # Send reply to server
        player.c.send(pickle.dumps(package))

        # Listen for reply
        self.s.listen(5)
        print('Listening..')
        while True:
            # Getting a reply from the player
            recive = player.c.recv(1024)
            package = pickle.loads(recive)
            clientMessage = package[key].decode()
            print(player.name, 'sent:', key, '->', clientMessage)
            return clientMessage

    def isGameReady(self) -> bool:
        if self.minPlayers <= len(self.players) and self.host and self.status != 'playing':
            print('Game ready. Request host (' + self.gameHost.name + ') to start')
            if self.request(self.gameHost, 'none', 'startGameRequest') == 'True':
                self.startGame()
        return False

    def startGame(self):
        print('START GAME!!')
        self.status = 'playing'

        # Message all players that the game has started
        for player in self.players:
            self.sendMessage(player, 'Game has started!')

        # Send image to all players
        for player in self.players:
            self.request(player, self.memeImage.image, 'imageTextRequest')

    def makeMeme(self, memeImage: MemeImage, players: Player) -> [MemeImage]:
        pass

    def getScore(self, memeImage: MemeImage, players: Player) -> [int]:
        for player in players:
            self.request(player, 'scoreRequest', 'none')
        pass

    def setGameHost(self, player: Player):
        self.gameHost = player

    def kill(self):
        self.c.close()
