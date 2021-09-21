# https://www.tutorialspoint.com/python/python_networking.htm
import socket, pickle  # Import socket module


class Player:
    def __init__(self, port):
        self.s = socket.socket()  # Create a socket object
        self.host = socket.gethostname()  # Get local machine name
        self.port = port  # Reserve a port for your service.

        self.s.connect((self.host, self.port))
        print(self.s.recv(1024).decode("utf-8"))

    def listen(self):
        while True:
            serverMessage = self.s.recv(1024).decode("utf-8")
            if serverMessage:
                print(serverMessage)
                if serverMessage == 'nameRequest':
                    print('Hi! What is your name?')
                    name = input('Type your name here: ')
                    self.sendMessage('name', name)
                    print('Hi,', name + '!')

    def sendMessage(self, key: str, message: str):
        package = {key: message.encode()}
        self.s.send(pickle.dumps(package))

    def kill(self):
        self.s.close()


client = Player(1024)
client.listen()
