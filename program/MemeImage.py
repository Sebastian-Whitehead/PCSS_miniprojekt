import random
import os, os.path
import cv2

# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import threading
import time


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

# Splits longer strings in to two lines
def split_string(input_text, img, font):
    if img.size[0] < font.getsize(input_text)[
        0]:  # Is the total string width in specified font and size wider than the image
        strings_list = input_text.split()  # Split input_text into list of words
        strings_added = 0  # Number of words put into the test string
        testLine = ""  # Test String to find splitting point of input_text

        # Append string word by word until it surpasses width of image
        while img.size[0] - 10 > font.getsize(testLine)[0]:
            testLine += f"{strings_list[strings_added]} "
            strings_added += 1

        # Set blank lines
        line1 = ""
        line0 = ""

        # Append line1 with one less word than the previous test line
        for i in range(strings_added - 1):
            line1 += f"{strings_list[i]} "

        # Append the remaining words to line 0
        for i in range(len(strings_list) - (strings_added - 1)):
            line0 += f"{strings_list[i + (strings_added - 1)]} "

        return line1, line0
    else:  # If string splitting is not needed return input text in line1 and a blank line0
        line1 = input_text
        line0 = ""
        return line1, line0

# Edit imput text onto image
def edit_image(input_path, player_id, input_text):

    img = Image.open(f'./images/{input_path}')  # Open an Image
    I1 = ImageDraw.Draw(img)  # Call draw Method to add 2D graphics in an image
    Font = 'ComicSansMS3.ttf'
    TextSize = 40
    myFont = ImageFont.truetype(Font, TextSize)  # Custom font style and font size

    if img.size[0] * 2 < myFont.getsize(input_text)[0]:
        print("to much text!")
    else:
        # Split into two lines if input string is to long for 1
        input_text1, input_text0 = split_string(input_text, img, myFont)

        # Calculate Text locations
        textX = img.size[0] / 2 - myFont.getsize(input_text0)[0] / 2
        textY = img.size[1] - myFont.getsize(input_text0)[1] - 10

        I1.text((textX, textY), input_text0, font=myFont, fill=(100, 100, 100))

        # If there is text in teh second line
        if len(input_text1) > 0:
            # calculate Text Location
            textX = img.size[0] / 2 - myFont.getsize(input_text1)[0] / 2
            textY -= myFont.getsize(input_text1)[1] - 5

            I1.text((textX, textY), input_text1, font=myFont, fill=(100, 100, 100))

        # preview image
        img.show()

        # Save the edited image
        img.save(f"./playerImages/{player_id}-{input_path}")
        print(f"Image Saved = ./playerImages/{player_id}-{input_path}")

# Retrieves the path of a submitted image
def retrieve_PI_path(imageToRetrieve, player_id):
    img = f"./playerImages/{player_id}-{imageToRetrieve}"
    return img


if __name__ == '__main__':

    CurrentImgPath = "star.png"

    threading.Thread(target=edit_image, args=(CurrentImgPath, 1, "short meme text")).start()
    threading.Thread(target=edit_image, args=(CurrentImgPath, 2, "This is a longer meme text to testing weather the line splitting function still works")).start()

    memeImage = MemeImage()