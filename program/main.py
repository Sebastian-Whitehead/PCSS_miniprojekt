# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Open an Image
img = Image.open('car.png')

# Call draw Method to add 2D graphics in an image
I1 = ImageDraw.Draw(img)

# Custom font style and font size
myFont = ImageFont.truetype('ComicSansMS3.ttf', 65)

# Add Text to an image
I1.text((10, 10), "The Quick Brown Fox Jumped Over The Lazy Dog", font=myFont, fill=(255, 150, 60))

# Display edited image
img.show()

# Save the edited image
img.save("car2.png")