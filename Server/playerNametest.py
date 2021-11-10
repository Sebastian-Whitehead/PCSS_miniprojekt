class Player:
    size = 0

    def __init__(self):
        self.name = Player.size
        Player.size += 1

players = []
for player in range(4):
    player = Player()
    players.append(player)
print(players)

names = [player.name for player in players]
print(names)