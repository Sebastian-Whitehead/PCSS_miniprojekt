import socket, pickle, json


class Client():

    # Initial setup
    def __init__(self):
        self.texts = []
        self.memeImage = 'work.jpg'
        self.memelist = []
        self.winner = -1

    # Connect the client to the server
    def connectToServer(self, IP, name):
        print('Connecting to server..')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 1024
        self.IP = IP

        if not self.IP:
            print("**IP FIELD IS BLANK --> CONNECTING TO LOCAL HOST!**")
            self.s.connect((self.host, self.port))
        else:
            self.s.connect((self.IP, self.port))

        # Start listen for messages from the server
        # (Needs two)
        serverKey = self.listen()
        print(f'{serverKey=}')
        serverKey = self.listen()
        print(f'{serverKey=}')

        # Let all other players wait for the game to start
        if serverKey[0] == 'nameRequest':
            self.sendMessage('nameRequest', name)

    """
    # Request the game host to start the game
    def startGameRequest(self, serverKey: str):
        print('Start game request received')
    """

    # Listens for request or message from the server
    def listen(self) -> tuple:
        print('Listening..')
        while True:
            receive = self.s.recv(1024)  # Receiving a request or message
            print(receive)
            if len(receive) < 1: print(f'{receive=} (empty)')
            package = pickle.loads(receive)  # Loack package using pickle
            serverKey = list(package)[0]  # Get the key from the package
            # Get the message from the package using json and decode
            serverMessage = json.loads(package[serverKey].decode("utf-8"))

            if serverKey:
                print('ServerKey:', serverKey, '->', serverMessage)
                return [serverKey, serverMessage]  # Return key and message tuple

    # Send message to the server with a matching key
    def sendMessage(self, key: str, message: str):
        print('Sending', message, '->', key)
        package = {key: message.encode()}  # Packages the message with a matching key
        self.s.send(pickle.dumps(package))  # Send reply to server

        print('')

    # Close Client Function
    def kill(self):
        self.s.close()


if __name__ == '__main__':
    Client()
