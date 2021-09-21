# https://www.tutorialspoint.com/python/python_networking.htm
import socket, pickle  # Import socket module

class Client:
    def __init__(self, port):
        self.s = socket.socket()
        self.host = socket.gethostname()
        self.port = port
        self.s.connect((self.host, self.port))
        print(self.s.recv(1024).decode("utf-8"))

        self.listen()

    def listen(self):
        # Listens for request or message from the server
        while True:
            # Receiving a request or message
            serverMessage = self.s.recv(1024).decode("utf-8")
            if serverMessage:
                if serverMessage == 'nameRequest':
                    self.promptReply(serverMessage, 'Hi! What is your name?. Type your name here')
                elif serverMessage == 'startGameRequest':
                    self.promptReply(serverMessage, 'Enough players to start the game. Type "True" to start the game')
                else:
                    print(serverMessage)

    def promptReply(self, key: str, UIMessage: str):
        # Prompts the user for a reply
        message = input(UIMessage + ': ')
        # Packages the message with a matching key
        package = {key: message.encode()}
        # Send reply to server
        self.s.send(pickle.dumps(package))

    def kill(self):
        self.s.close()

client = Client(1024)