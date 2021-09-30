import socket, pickle, json, threading
from Player import Player
from GameEngine import GameEngine
from SendReceiveImage import SendReceiveImage
from ClientThread import ClientThread

""" MISSING:
- Player disconnect
- Host disconnect 
"""

class Server(GameEngine, SendReceiveImage):
    def __init__(self, port):
        super().__init__()

        # Start server
        self.s = socket.socket()
        self.host = socket.gethostname()
        self.port = port
        self.s.bind((self.host, self.port))
        print(self.s, 'Server is Running..')
        print('')

        # Start game in lobby
        self.status = 'inLobby'
        self.feedback = 0
        self.run()

    def run(self):
        self.s.listen(5)
        while True:

            # Server listens for players joining the server
            player = Player()
            player.c, player.addr = self.s.accept()
            print('Got connection from:', player.addr)
            self.sendMessage(player, 'Thank you for connecting.', 'message')
            self.clientJoined(player)

            self.gameRunning(self)
        #self.s.close()

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
        if message == 'none' or type(message) != str:
            print('Sending:', '"' + key + '"', 'to', player.getName())
        else:
            print('Sending:', '"' + message + '"', 'to', player.getName())
        message = json.dumps(message).encode()
        package = {key: message} # Packages the message with a matching key
        player.c.send(pickle.dumps(package)) # Send reply to server

    def request(self, player: Player, message: [str], key: str) -> str:
        self.sendMessage(player, message, key)
        return self.listen(player, key)

    def listen(self, player: Player, key: str):
        # Listen for reply
        self.s.listen(5)
        print('Listening..')
        while True:
            # Getting a reply from the player
            receive = player.c.recv(1024)
            if receive is not None:
                package = pickle.loads(receive)
                clientMessage = package[key].decode()
                print(player.getName(), 'sent:', key, '->', clientMessage)
                return clientMessage

    def setGameHost(self, player: Player):
        self.gameHost = player

    def getGameHost(self) -> Player:
        return self.gameHost

    def kill(self):
        self.c.close()