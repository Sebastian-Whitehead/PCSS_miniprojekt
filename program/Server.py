# https://www.tutorialspoint.com/python/python_networking.htm
import socket, pickle  # Import socket module
import MemeImage

class Player:
    def __init__(self):
        self.name = False

class Server:
    def __init__(self, port):
        self.status = 'booting'
        self.minPlayers = 1
        self.gameHost = False
        self.players = []
        # self.memeImage = MemeImage()

        self.s = socket.socket()             # Create a socket object
        self.host = socket.gethostname()     # Get local machine name
        self.port = port                     # Reserve a port for your service.
        self.s.bind((self.host, self.port))  # Bind to the port
        print(self.s, 'Server is Running..')

    def run(self):
        self.s.listen(5)  # Now wait for player connection.
        while True:
            self.isGameReady()

            player = Player()
            player.c, player.addr = self.s.accept()  # Establish connection with player.
            print('Got connection from:', player.addr)
            player.c.send(b'Thank you for connecting.')
            self.clientJoined(player)

    def startGame(self):
        print('START GAME!!')
        self.status = 'playing'
        message = ('Game has started!').encode()
        for player in self.players:
            player.c.send(message)

    def clientJoined(self, newPlayer):
        for player in self.players:
            if newPlayer.addr == player.addr:
                return print('Old player')
        print('New player')
        name = self.request(newPlayer, 'name')
        newPlayer.name = name
        self.players.append(newPlayer)

        # Confirm player
        message = ('Hi, ' + newPlayer.name + '!').encode()
        newPlayer.c.send(message)

        if not self.gameHost:
            self.gameHost = newPlayer
            print('Host:', newPlayer.name)

    def request(self, player: Player, key: str):
        print('Requesting:', key)
        message = (key + 'Request').encode()
        player.c.send(message)
        self.s.listen(5)
        print('Listening..')
        while True:
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

    def getImage(self):
        pass

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

    def kill(self):
        self.c.close()
