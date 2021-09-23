import random

class MemeImage:
    images = ['star.png']

    def __init__(self):
        self.image = random.choice(self.images)