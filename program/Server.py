# https://www.tutorialspoint.com/python/python_networking.htm
import socket, pickle
from MemeImage import MemeImage
from Player import Player

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

        self.run()

    def run(self):
        self.s.listen(5)
        while True:
            self.isGameReady()

            # Server listens for players joining the server
            player = Player()
            player.c, player.addr = self.s.accept()
            print('Got connection from:', player.addr)
            player.c.send(b'Thank you for connecting.')
            self.clientJoined(player)

    def clientJoined(self, newPlayer):
        # Check if the user is already connected
        for player in self.players:
            if newPlayer.addr == player.addr:
                return print('Old player')

        # Request the name of the player
        name = self.request(newPlayer, 'name')
        newPlayer.setName(name)
        self.players.append(newPlayer)
        print('New player')

        # Confirm player with a message
        message = ('Hi, ' + newPlayer.name + '!').encode()
        newPlayer.c.send(message)

        # Set player to be game host if none
        if not self.gameHost:
            self.setGameHost(newPlayer)
            print('Host:', newPlayer.name)

    def request(self, player: Player, key: str) -> str:
        # Send request message to player
        print('Requesting:', key)
        message = (key + 'Request').encode()
        player.c.send(message)

        # Listen for reply
        self.s.listen(5)
        print('Listening..')
        while True:
            # Getting a reply from the player
            recive = player.c.recv(1024)
            message = pickle.loads(recive)
            decodeMessage = message[key + 'Request'].decode()
            print(player.name, 'sent:', key, '->', decodeMessage)
            return decodeMessage

    def isGameReady(self) -> bool:
        if self.minPlayers <= len(self.players) and self.host and self.status != 'playing':
            print('Game ready. Request host (' + self.gameHost.name + ') to start')
            if self.request(self.gameHost, 'startGame') == 'True':
                self.startGame()
        return False

    def startGame(self):
        print('START GAME!!')
        self.status = 'playing'

        # Message all players that the game has started
        message = ('Game has started!').encode()
        for player in self.players:
            player.c.send(message)

    def getText(self, memeImage: MemeImage, players: Player) -> MemeImage:
        for player in players:
            self.request(player, 'imageText')
        pass

    def makeMeme(self, memeImage: MemeImage, players: Player) -> [MemeImage]:
        pass

    def getScore(self, memeImage: MemeImage, players: Player) -> [int]:
        for player in players:
            self.request(player, 'score')
        pass

    def setGameHost(self, player: Player):
        self.gameHost = player

    def kill(self):
        self.c.close()
