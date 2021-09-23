import random
import os
import cv2

class RandomMemeImage:

    def getRandomImage():
        path = "C:\\Users\\Charlotte Johansen\\PycharmProjects\\miniprojectProgramming\\.memes"
        files = os.listdir(path)
        d = random.choice(files)
         # os.startfile(d)
        ran = cv2.imread(d)
        ran = cv2.resize(ran, (640, 640))
        cv2.imshow("hej", ran)
        cv2.waitKey(0)

    getRandomImage()

class MemeImage:
    images = ['star.png']

    def __init__(self):
        self.image = random.choice(self.images)
