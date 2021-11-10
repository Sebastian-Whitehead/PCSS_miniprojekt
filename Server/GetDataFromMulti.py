import multiprocessing, random

playersSize = 4

class Player:
    size = 0
    def __init__(self, id):
        self.answer = random.randint(0, 9)
        self.id = Player.size
        Player.size += 1

class GameEngine:
    def __init__(self):
        self.players = []
        for player in range(playersSize):
            player = Player(len(self.players))
            self.players.append(player)
        self.feedback = 0
        self.points = []

    def makeMulti(self):
        t = {}
        FB = multiprocessing.Value('i', 0)
        ans = multiprocessing.Array('i', range(len(self.players)))

        # Request score from players
        for pos, player in enumerate(self.players):
            # start a thread for each player that requests score and listens for an answer
            t[pos] = multiprocessing.Process(
                target=self.multiThreadFunction, args=(player, FB, ans)
            )
            t[pos].start()

        for pos in t:  # After all threads are started begin to join the threads 1 by one
            t[pos].join()  # Wait for thread to complete then join

        self.feedback = FB.value
        self.points.extend(ans)

        print(f'{self.feedback=}, {self.points=}, {FB.value=}')
        print(f'{ans[:]=}, {self.points=}, {FB.value=}')
        print()


    def multiThreadFunction(self, player, feedback, answer):

        print(f'{player.id=}')
        print(f'{player.answer=}')

        # Append the score to list
        #answer.append = int(player.answer)
        answer[player.id] = player.answer

        print(f'{answer[:]=}')
        print()

        # TODO: ADD WAITING FOR OTHER PLAYERS SCREEN HERE
        # Add feedback to continue
        feedback.value += 1


if __name__ == '__main__':
    GameEngine().makeMulti()
