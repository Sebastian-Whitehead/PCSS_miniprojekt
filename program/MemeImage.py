import random
import os
import cv2

class MemeImage:
    path = "C:\\Users\\Charlotte Johansen\\PycharmProjects\\miniprojectProgramming\\.memes"

    def __init__(self):
        self.image = random.choice(self.images)

    def getRandomImage(self, path: str) -> str:
        files = os.listdir(path)
        d = random.choice(files)
         # os.startfile(d)
        #ran = cv2.imread(d)
        ran = d
        #ran = cv2.resize(ran, (640, 640))
        #cv2.imshow("hej", ran)
        #cv2.waitKey(0)

        return ran