import cv2

def sliceImage(image):
    print(image)
    for x, row in enumerate(image):
        print(str(row))

star = cv2.imread('star.png')
sliceImage(star)