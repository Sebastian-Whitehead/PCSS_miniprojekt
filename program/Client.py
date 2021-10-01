import socket, pickle, cv2, json
from SendReceiveImage import SendReceiveImage

def makeImage(image, text: str):
    return image

class Client(SendReceiveImage):
    # Initial setup
    def __init__(self, port):
        self.s = socket.socket()
        self.host = socket.gethostname()
        self.port = port
        self.s.connect((self.host, self.port))
        self.images = []

        self.listen()

    # Listens for request or message from the server
    def listen(self):


        while True:

            # Receiving a request or message
            receive = self.s.recv(1024)
            package = pickle.loads(receive)
            serverKey = list(package)[0]
            serverMessage = json.loads(package[serverKey].decode("utf-8"))
            if serverKey:
                if serverKey == 'nameRequest': # Server is requesting player name
                    self.promptReply(serverKey, 'Hi! What is your name?. Type your name here')

                elif serverKey == 'startGameRequest': # Requesting host to start game
                    self.promptReply(serverKey, 'Enough players to start the game. Type "True" to start the game')

                elif serverKey == 'imageTextRequest': # Requesting text for image
                    frame_data = self.receiveImage(self.s)
                    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

                    # Show image
                    #cv2.imshow('ImageWindow', frame)
                    #cv2.waitKey(0)

                    imageText = self.promptReply(serverKey, 'Type text to image')
                    if 0 < len(imageText):
                        imageWithText = makeImage(frame, imageText)
                        self.sendImage(imageWithText, self.s)

                elif serverKey == 'imageScoreRequest': # Requesting player to pick the best image

                    for i in range(0, int(serverMessage) + 1):
                        frame_data = self.receiveImage(self.s)
                        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                        self.images.append(frame)

                    for pos, image in enumerate(self.images):
                        cv2.imshow('Image ' + str(pos), image)
                    cv2.waitKey(0)
                    self.promptReply(serverKey, 'Type in the number of the best meme')

                elif serverKey == 'message': #Recieveing text message from server
                    print(serverMessage)
                    print('')

                else:
                    print('Unknown message from server..')

    # Prompts user for specified reply from "listen"
    def promptReply(self, key: str, UIMessage: str):
        message = input(UIMessage + ': ')  # Prompts the user for a reply
        package = {key: message.encode()}  # Packages the message with a matching key
        self.s.send(pickle.dumps(package))  # Send reply to server
        print('')
        return message

    # Close Function
    def kill(self):
        self.s.close()

client = Client(1024)
