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
        self.imageName = random.choice(files)
        randomImage = MemeImage.path + '/' + self.imageName
        self.image = cv2.imread(randomImage)

    # Get current picked image
    def getImage(self) -> str:
        return self.image

    def getImageName(self) -> str:
        return self.imageName


if __name__ == '__main__':
    memeImage = MemeImage()
