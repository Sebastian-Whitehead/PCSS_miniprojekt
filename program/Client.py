# https://www.tutorialspoint.com/python/python_networking.htm
import socket, pickle  # Import socket module

class Client:
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
                if serverMessage == 'nameRequest':
                    print('Hi! What is your name?')
                    self.sendMessage(serverMessage, 'Type your name here')
                elif serverMessage == 'startGameRequest':
                    print('Enough players to start the game.')
                    self.sendMessage(serverMessage, 'Type "True" to start the game')
                else:
                    print(serverMessage)

    def sendMessage(self, key: str, UIMessage: str):
        message = input(UIMessage + ': ')
        package = {key: message.encode()}
        self.s.send(pickle.dumps(package))

    def kill(self):
        self.s.close()

client = Client(1024)
client.listen()