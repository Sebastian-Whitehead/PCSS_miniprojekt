import random
import os, os.path

class MemeImage:
    path = "images"

    def __init__(self):
        self.image = self.getRandomImage(self.path)

    def getRandomImage(self, path: str) -> str:
        files = os.listdir(path)
        randomImage = random.choice(files)
        return randomImage

    def getImage(self) -> str:
        return self.image

memeImage = MemeImage()
print(memeImage.getImage())