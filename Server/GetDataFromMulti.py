import multiprocessing, random, string

playersSize = 4
letter_count = 10

class Player:
    size = 0
    def __init__(self):
        self.answer = random.randint(0, 9)
        self.text = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
        print(self.text)
        self.id = Player.size
        Player.size += 1

class GameEngine:
    def __init__(self):
        self.players = []
        for player in range(playersSize):
            player = Player()
            self.players.append(player)
        self.feedback = 0
        self.points = []

        self.makeMulti('i', 'answer')
        self.makeMulti('c_char', 'text')

    def makeMulti(self, type, target):
        t = {}
        FB = multiprocessing.Value('i', 0)

        array = []
        for player in range(len(self.players)):
            inArray = []
            if type == 'i':
                inArray = 0
            elif type == 'c_char':
                inArray = ['' for i in range(10)]
            array.append(inArray)
        ans = multiprocessing.Array(type, array)

        # Request score from players
        for pos, player in enumerate(self.players):
            # start a thread for each player that requests score and listens for an answer
            t[pos] = multiprocessing.Process(
                target=self.multiThreadFunction, args=(player, target, FB, ans)
            )
            t[pos].start()

        for pos in t:  # After all threads are started begin to join the threads 1 by one
            t[pos].join()  # Wait for thread to complete then join

        self.feedback = FB.value
        self.points.extend(ans)

        print(f'{self.feedback=}, {self.points=}, {FB.value=}')
        print(f'{ans[:]=}, {self.points=}, {FB.value=}')
        print()


    def multiThreadFunction(self, player, target, feedback, answer):

        print(f'{player.id=}')
        print(f'{player.answer=}')

        # Append the score to list
        value = getattr(player, target)
        if target == 'points':
            answer[player.id] = value
        elif target == 'text':
            for char in value:
                print(char)

        print(f'{answer[:]=}')
        print()

        # TODO: ADD WAITING FOR OTHER PLAYERS SCREEN HERE
        # Add feedback to continue
        feedback.value += 1


if __name__ == '__main__':
    GameEngine()
