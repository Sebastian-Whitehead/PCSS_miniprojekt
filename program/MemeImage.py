import random
import os, os.path
import cv2

# Meme image class for handling images
class MemeImage:
    path = "images"

    def __init__(self):
        self.newRandomImage()

    # Get a random image from the folder
    def newRandomImage(self) -> str:
        files = os.listdir(MemeImage.path)
        randomImage = MemeImage.path + '/' + random.choice(files)
        self.image = cv2.imread(randomImage)

    # Get current picked image
    def getImage(self) -> str:
        return self.image

def makeImageToMeme():
    pass

if __name__ == '__main__':
    memeImage = MemeImage()
    print(memeImage.getImage())