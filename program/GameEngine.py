import threading
import time

import cv2
import threading
from ClientThread import ClientThread

from MemeImage import MemeImage


class GameEngine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.players = []  # All players that are currently on the server (Keeps on disconnect)
        self.memeImage = MemeImage()  # Meme image (Not implemented)

        self.minPlayers = 1  # Minimum players on the server before the game can start
        self.gameHost = False  # The game host
        self.setStatus('booting')

    def run(self):
        print
        "Starting " + self.name
        # print_time(self.name, 5, self.counter)
        # print
        "Exiting " + self.name

    def gameRunning(self, server):
        self.isGameReady(server)
        self.imageScoreRequest(server)
        self.handlingScore(server)

    def isGameReady(self, server) -> bool:
        if self.minPlayers <= len(self.players) and self.host and self.status == 'inLobby':
            print('Game ready. Request host (' + self.getGameHost().getName() + ') to start')
            gameStart = self.request(self.getGameHost(), 'none', 'startGameRequest')
            if gameStart == 'True':
                self.startGame(server)
            else:
                self.isGameReady(server)
        return False

    def startGame(self, server):
        print('START GAME!!')
        self.setStatus('imageTextRequest')

        # Send image to all players
        for player in self.players:
            server.sendMessage(player, 'Game has started!', 'message')
            print('')

            server.sendMessage(player, 'imageTextRequest', 'message')

            threads = []

            thread1 = threading.Thread(
                target=server.sendImage,
                args=(self.memeImage.image, player.c)
            )

            thread1.start()
            threads.append(thread1)
            thread1.join()

            thread2 = threading.Thread(
                target=server.listen,
                args=(player, 'imageTextRequest')
            )
            thread2.start()
            threads.append(thread2)

            while thread2 is None:
                print('No result')

            thread2.join()

            player.image = server.receiveImage(player.c)
            if player.image != False:
                self.feedback += 1

        print('')

    def imageScoreRequest(self, server):
        if len(self.players) <= self.feedback and self.status == 'imageTextRequest':
            print('All players has send their image text')
            self.setStatus('imageScoreRequest')

            # Request score from players
            for pos, player in enumerate(self.players):
                server.sendMessage(player, len(server.players), 'imageScoreRequest')
                eachPlayer = 0
                #while eachPlayer <= len(self.players) - 1:
                for eachPlayer, image in enumerate(self.players):
                    if self.players[eachPlayer].image != False:
                        thread1 = threading.Thread(
                            target=server.sendImage,
                            args=(self.players[eachPlayer].image, player.c)
                        )
                        thread1.start()
                        thread1.join()
                        eachPlayer += 1

                if len(self.players) - 1 <= pos:
                    thread2 = threading.Thread(
                        target=server.listen,
                        args=(player, 'imageTextRequest')
                    )
                    thread2.start()
                    thread2.join()
                server.receiveImage(player.c)

            print('')

    def handlingScore(self, server):
        if len(self.players) <= self.feedback and self.status == 'imageScoreRequest':
            print('All players has send their opinion')
            self.setStatus('handlingScore')

            # Handling score
            print('Handling score..')

            """ CODE MISSING """

            winner = "'pass'"
            print('')

            # Sending winner to all players
            for player in self.players:
                server.sendMessage(player, 'Winner is ' + winner + '!', 'message')
            print('')

            # Request new game
            print('Requesting new game..')
            print('')
            self.memeImage.newRandomImage()
            self.setStatus('inLobby')
            return server.run()

    def setStatus(self, status: str) -> bool:
        self.status = status
        self.feedback = 0
        return True
