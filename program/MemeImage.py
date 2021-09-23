import random
import os, os.path

class MemeImage:
    path = "images"

    def __init__(self):
        self.image = self.getRandomImage()

    def getRandomImage(self) -> str:
        files = os.listdir(self.path)
        randomImage = self.path + '/' + random.choice(files)
        return randomImage

    def getImage(self) -> str:
        return self.image

def testCode():
    memeImage = MemeImage()
    print(memeImage.getImage())

#testCode()