class Player:
    def __init__(self):
        self.name = False

    def setName(self, name: str):
        self.name = name

    def getName(self) -> str:
        return self.name