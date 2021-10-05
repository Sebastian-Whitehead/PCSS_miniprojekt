import threading

# Player class used as client
class Player():
    size = 0        # Amount of players in the game
    meme = False    # Meme made by player

    def __init__(self):
        #threading.Thread.__init__(self)
        self.name = False
        self.ID = Player.size
        Player.size += 1

    # Setter for player name
    def setName(self, name: str):
        self.name = name

    # Getter for player name
    def getName(self) -> str:
        return self.name