import threading

class Player():#threading.Thread):
    size = 0

    def __init__(self):
        #threading.Thread.__init__(self)
        self.name = False
        self.ID = Player.size
        Player.size += 1

    def setName(self, name: str):
        self.name = name

    def getName(self) -> str:
        return self.name