import socket, pickle, json
#from program.SendReceiveImage import SendReceiveImage
#from program.MemeImage import makeImageToMeme

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
        serverKey = self.listen()
        serverKey = self.listen()

        print(f'{serverKey=}')



        # Let all other players wait for the game to start
        if serverKey[0] == 'nameRequest':
            self.sendMessage('nameRequest', name)

    """
=======
        # TODO: PROMT PLAYER FOR NUNBER
        #serverKey = self.listen()
        #print(f'{serverKey=}')

        #if serverKey[0] == 'totalPlayersRequest':
        #    self.sendMessage('totalPlayersRequest', str(self.totalExpectedPlayers))

        #TODO: PROMT PLAYER FOR GAME START

>>>>>>> 21518ebcb36dce37fb2778645630ed7d2544bf49
    # Request the game host to start the game
    def startGameRequest(self, serverKey: str):
        print('Start game request received')
    """
    """
    # Random image sent to player. Prompt player for a text to put to the image -> image with text
    # NOT USED
    def imageTextRequest(self, serverKey: str, imageText: str):
        # Receive and decrypt image
        frame_data = self.receiveImage(self.s)
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        # Show image
        # cv2.imshow('ImageWindow', frame)
        # cv2.waitKey(0)

        # Request player for text to put onto the image
        # imageText = input(serverKey, 'Type text to image')
        if 0 < len(imageText):
            self.meme = makeImageToMeme(frame, imageText)  # Make meme using the text and image
            self.sendImage(self.meme, self.s)  # Send meme to server

    # Show all memes to the player and ask for a personal favorite
    # NOT USED
    def imageScoreRequest(self, serverKey: str, serverMessage: str):
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
    # NOT USED
    def message(self, serverMessage: str):
        print(serverMessage)
        print('')
    """

    # Listens for request or message from the server
    def listen(self) -> tuple:
        print('Listening..')
        while True:
            # Receiving a request or message
            receive = self.s.recv(1024)
            print(receive)
            if len(receive) < 1:
                print(f'{receive=} (empty)')
            # Loack package using pickle
            package = pickle.loads(receive)
            # Get the key from the package
            serverKey = list(package)[0]
            # Get the message from the package using json and decode
            serverMessage = json.loads(package[serverKey].decode("utf-8"))

            if serverKey:
                print('ServerKey:', serverKey, '->', serverMessage)
                # Return key and message tuple
                return [serverKey, serverMessage]

    """
    # Prompt the player for a reply it can send to the server
    # NOT USED
    def promptReply(self, key: str, UIMessage: str):
        # Prompts the user for a reply
        message = input(UIMessage + ': ')
        # Send key and message to the server
        self.sendMessage(key, message)
    """

    # Send message to the server with a matching key
    def sendMessage(self, key: str, message: str):
        print('Sending', message, '->', key)
        # Packages the message with a matching key
        package = {key: message.encode()}
        # Send reply to server
        self.s.send(pickle.dumps(package))
        print('')

    # Close Function
    def kill(self):
        self.s.close()


if __name__ == '__main__':
    Client()
