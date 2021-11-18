import socket, pickle, json, threading
from Player import Player
from GameEngine import GameEngine
from SendReceiveImage import SendReceiveImage

""" MISSING:
- Player disconnect
- Host disconnect 
"""


# Server class. Connects with client
class Server(GameEngine, SendReceiveImage):

    # Initital Function Starts Server & Game Lobby
    def __init__(self, port):
        super().__init__()

        # Setup server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = port
        self.s.bind((self.host, self.port))
        print(self.s, 'Server is Running..')
        print('')

        # Setup game in lobby
        self.status = 'inLobby'
        self.feedback = 0

        # Run server and game, start listen
        self.run()

    # Server Starts Listening for players joining the server
    def run(self):
        self.s.listen(5)
        print('Listening..')

        # While Listening

        while True:

            print('Listening for players..')

            # Server listens for players joining the server
            player = Player()
            player.c, player.addr = self.s.accept()
            # Respond acceptance to client
            print('Got connection from:', player.addr)
            self.sendMessage(player, 'Thank you for connecting.', 'accept')
            # Handle new player to server
            self.clientJoined(player)

            # Game engine running
            self.gameRunning(self)

            self.run()

    # Player sends connect message, Check if they are a new player
    def clientJoined(self, newPlayer):
        # Check if the user is already connected
        for player in self.players:
            if newPlayer.addr == player.addr:
                # Handle old player connecting again
                # (Does not do anything at the moment MISSING)
                return print('Old player')

        # Set name of player by player input
        playerName = self.request(newPlayer, ['getPlayerName'], 'nameRequest')
        newPlayer.setName(playerName)

        # Add new player to server
        self.players.append(newPlayer)
        print('New player:', newPlayer.name)

        # Set player to be game host if there is none
        if not self.getGameHost():
            self.setGameHost(newPlayer)
            print('Host:', newPlayer.getName())

        print('')

    # Send message to specified player
    def sendMessage(self, player: Player, message: [str], key: str):
        # Print message or key to console
        print(f'Sending: "{key}" to {player.getName()}')
        if message != 'none' or type(message) == str:
            print(f'Message: "{message}"')
        # Encode message to json
        message = json.dumps(message).encode()
        # Packages the message with a matching key
        package = {key: message}
        # Send message to client with socket
        player.c.send(pickle.dumps(package))

    # Send data request/ Response to client
    def request(self, player: Player, message: [str], key: str) -> str:
        # Send message to client using method
        self.sendMessage(player, message, key)
        # Listen for reply from client with same key as sent
        return self.listen(player, key)

    # Listen for response to data request
    def listen(self, player: Player, key: str):
        # Listen for reply from client
        self.s.listen(5)
        print('Listening..')
        while True:
            # Getting a reply from the player
            receive = player.c.recv(1024)
            if receive is not None:
                # Load the packages with pickle
                package = pickle.loads(receive)
                # Print package to console
                print(package)
                # Decode package using key
                clientMessage = package[key].decode()
                # Print message and key to console
                print(player.getName(), 'sent:', key, '->', clientMessage)
                # Return message
                return clientMessage

    # Setter for game host role
    def setGameHost(self, player: Player):
        self.gameHost = player

    # Getter for game host role
    def getGameHost(self) -> Player:
        return self.gameHost

    # Server Close Function
    def kill(self):
        self.c.close()


# Start server with the port 1024
if __name__ == '__main__':
    Server(1024)
