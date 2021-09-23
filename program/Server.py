import socket, pickle, json
from MemeImage import MemeImage
from Player import Player
from GameEngine import GameEngine

class Server(GameEngine):
    def __init__(self, port):
        super().__init__()
        self.players = []            # All players that are currently on the server (Keeps on disconnect)
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
            self.gameRunning()

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
            receive = player.c.recv(1024)
            if receive:
                package = pickle.loads(receive)
                clientMessage = package[key].decode()
                print(player.getName(), 'sent:', key, '->', clientMessage)
                self.feedback += 1
                return clientMessage

    def setGameHost(self, player: Player):
        self.gameHost = player

    def getGameHost(self) -> Player:
        return self.gameHost

    def kill(self):
        self.c.close()