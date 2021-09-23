# https://www.tutorialspoint.com/python/python_networking.htm
import socket, pickle  # Import socket module
import cv2

class Client:
    def __init__(self, port):
        self.s = socket.socket()
        self.host = socket.gethostname()
        self.port = port
        self.s.connect((self.host, self.port))

        self.listen()

    def listen(self):
        # Listens for request or message from the server
        while True:
            # Receiving a request or message
            recive = self.s.recv(1024)
            package = pickle.loads(recive)
            serverKey = list(package)[0]
            serverMessage = package[serverKey].decode("utf-8")
            if serverKey:
                if serverKey == 'nameRequest':
                    self.promptReply(serverKey, 'Hi! What is your name?. Type your name here')
                elif serverKey == 'startGameRequest':
                    self.promptReply(serverKey, 'Enough players to start the game. Type "True" to start the game')
                elif serverKey == 'imageTextRequest':
                    print('Image', serverMessage, 'recived.')
                    #image = cv2.imread(serverMessage)
                    #cv2.imshow(image)
                    #cv2.KeyWait(10000)
                    self.promptReply(serverKey, 'Type text to image')
                else:
                    print(serverMessage)

    def promptReply(self, key: str, UIMessage: str):
        message = input(UIMessage + ': ')  # Prompts the user for a reply
        package = {key: message.encode()}  # Packages the message with a matching key
        self.s.send(pickle.dumps(package))  # Send reply to server
        print('')

    def kill(self):
        self.s.close()


client = Client(1024)
