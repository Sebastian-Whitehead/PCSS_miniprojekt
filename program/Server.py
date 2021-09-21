# https://www.tutorialspoint.com/python/python_networking.htm
import socket, pickle  # Import socket module
import MemeImage
from Player import Player

class Server:
    def __init__(self, port):
        self.s = socket.socket()  # Create a socket object
        self.host = socket.gethostname()  # Get local machine name
        self.port = port  # Reserve a port for your service.
        self.s.bind((self.host, self.port))  # Bind to the port
        print(self.s)
        print('Server is Running..')

        self.players = []
        # self.memeImage = MemeImage()

    def run(self):
        self.s.listen(5)  # Now wait for player connection.
        while True:
            player = Player()
            player.c, player.addr = self.s.accept()  # Establish connection with player.
            print('Got connection from:', player.addr)
            try:
                player.c.send(b'Thank you for connecting')
                name = self.request(player, 'name')
                player.name = name
            except TypeError:
                print('TypeError')

    def request(self, player: Player, key: str):
        message = (key + 'Request').encode()
        player.c.send(message)
        self.s.listen(5)
        while True:
            recive = player.c.recv(1024)
            message = pickle.loads(recive)
            decodeMessage = message[key].decode()
            print(player, 'sent:', key, '->', decodeMessage)
            return decodeMessage

    def kill(self):
        self.c.close()
