import random
import os, os.path

class MemeImage:
    path = "images"

    def __init__(self):
        self.newRandomImage()

    def newRandomImage(self) -> str:
        files = os.listdir(MemeImage.path)
        randomImage = MemeImage.path + '/' + random.choice(files)
        self.image = randomImage

    def getImage(self) -> str:
        return self.image

def testCode():
    memeImage = MemeImage()
    print(memeImage.getImage())

#testCode()