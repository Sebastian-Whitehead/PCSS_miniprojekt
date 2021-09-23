import random
import os, os.path

class MemeImage:
    path = "images"

    def __init__(self):
        self.image = self.getRandomImage()

    def getRandomImage(self) -> str:
        files = os.listdir(self.path)
        randomImage = random.choice(files)
        return randomImage

    def getImage(self) -> str:
        return self.image

memeImage = MemeImage()
print(memeImage.getImage())