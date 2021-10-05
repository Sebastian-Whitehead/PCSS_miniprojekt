import socket, pickle, cv2, json
from SendReceiveImage import SendReceiveImage

def makeImageToMeme(image, text: str):
    return image

class Client(SendReceiveImage):
    # Initial setup
    def __init__(self):
        ip = input('Ip: ')
        name = input('name: ')
        self.connectToServer(ip, name)

    def connectToServer(self, ip, name):
        print('Connecting')
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 1024
        self.s.connect((self.host, self.port))
        self.memes = []                         # All images gotten from server made from other players

        self.listen()                           # Start listen for messages from the server

    # Request the player for a name or username
    def nameRequst(self, serverKey: str): self.promptReply(serverKey, 'Hi! What is your name?. Type your name here')

    # Request the game host to start the game
    def startGameRequest(self, serverKey: str): self.promptReply(serverKey, 'Enough players to start the game. Type "True" to start the game')

    # Random image sent to player. Prompt player for a text to put to the image -> image with text
    def imageTextRequst(self, serverKey: str):
        # Receive and decrypt image
        frame_data = self.receiveImage(self.s)
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        # Show image
        #cv2.imshow('ImageWindow', frame)
        #cv2.waitKey(0)

        # Request player for text to put onto the image
        imageText = input(serverKey, 'Type text to image')
        if 0 < len(imageText):
            self.meme = makeImageToMeme(frame, imageText)   # Make meme using the text and image
            self.sendImage(self.meme, self.s)               # Send meme to server

    # Show all memes to the player and ask for a personal favorite
    def imageScoreRequst(self, serverKey: str, serverMessage: str):
        # Receive all memes from the server
        for i in range(0, int(serverMessage) + 1):
            frame_data = self.receiveImage(self.s)
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            self.memes.append(frame)

        # Show all memes
        for pos, meme in enumerate(self.memes):
            if meme is not self.meme:  # Filter the players own meme
                pass

        # Ask player for a favorite meme
        self.promptReply(serverKey, 'Type in the number of the best meme')

    # Show message to player
    def message(self, serverMessage: str):
        print(serverMessage)
        print('')

    # Listens for request or message from the server
    def listen(self):
        while True:
            # Receiving a request or message
            receive = self.s.recv(1024)
            package = pickle.loads(receive)
            serverKey = list(package)[0]
            serverMessage = json.loads(package[serverKey].decode("utf-8"))
            if serverKey:
                if serverKey == 'nameRequest': self.nameRequst(serverKey)
                elif serverKey == 'startGameRequest': self.startGameRequest(serverKey)
                elif serverKey == 'imageTextRequest': self.imageTextRequst(serverKey)
                elif serverKey == 'imageScoreRequest': self.imageScoreRequst(serverKey, serverMessage)
                elif serverKey == 'message': self.message()
                else: print('Unknown message from server..') # Error message to console, no key found

    # Prompt the player for a reply it can send to the server
    def promptReply(self, key: str, UIMessage: str):
        message = input(UIMessage + ': ')               # Prompts the user for a reply
        package = {key: message.encode()}               # Packages the message with a matching key
        self.s.send(pickle.dumps(package))              # Send reply to server
        print('')

    # Close Function
    def kill(self):
        self.s.close()

client = Client()