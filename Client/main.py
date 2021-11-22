import tkinter as tk
from tkinter import ttk, Entry
from PIL import Image, ImageTk
from Client import Client
from edit_image import edit_image, resizeImage
from handleHighScoreList import *

LARGEFONT = ("Verdana", 35)  # Font

""" # Manufactured data (start) #
players = 4
player_names = ["Rebecca", "Charlotte", "Tonko", "Tobias"]
# Manufactured data (end) # 
"""


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.client = Client()

        # creating a container
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.container = tk.Frame(self, )
        self.container.grid()

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # Make start page
        frame = StartPage(self.container, self, client=self.client)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        # Make page and go to it
        frame = cont(self.container, self, client=self.client)
        self.frames[cont] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        frame.tkraise()
        print('Showing frame', cont)


# Start game
class StartPage(tk.Frame, tkinterApp):
    def __init__(self, parent, controller, client):
        tk.Frame.__init__(self, parent)
        self.client = client

        # Adding labels, buttons, and pics c:
        label = ttk.Label(self, text="", font=LARGEFONT)
        label.grid(row=0, column=0, padx=10, pady=10)

        label = ttk.Label(self, text="Start Kenneth Kasse", font=LARGEFONT)
        label.place(relx=.5, rely=0.05, anchor="c")

        label = ttk.Label(self, text="Input your name")
        label.grid(row=1, column=0, padx=10, pady=10)

        # Name of player
        self.PName: Entry = tk.Entry(self)
        self.PName.grid(row=2, column=0, padx=10, pady=10)

        label = ttk.Label(self, text="IP")
        label.grid(row=3, column=0, padx=10, pady=10)

        # IP
        self.IPName: Entry = tk.Entry(self)
        self.IPName.grid(row=4, column=0, padx=10, pady=10)

        button1 = ttk.Button(self,
                             text="Join Game",
                             command=lambda: self.fetchStartPage(controller)
                             )
        button1.grid(row=5, column=0, padx=10, pady=10)

        meme = Image.open('work.jpg')
        meme = ImageTk.PhotoImage(meme)
        meme_lbl = tk.Label(self, image=meme)
        meme_lbl.image = meme
        meme_lbl.grid(row=6, column=0, padx=10, pady=10)

    # Connect to server button handle
    def fetchStartPage(self, controller):
        name = self.PName.get()  # Get written name in name input
        assert name != ""  # Code that doesnt continue the program if name field is empty.
        IP = self.IPName.get()  # Get written IP in IP input
        print(name, IP)
        self.client.connectToServer(IP, name)  # Connect to server with name and IP
        controller.show_frame(Page1)  # Continue to page 1

        # Listen for server
        serverKey = self.client.listen()
        if serverKey[0] == 'startGameRequest':  # Let the host listen for game start request
            controller.show_frame(hostPage)
        elif serverKey[0] == 'imageTextRequest':  # Let all other players wait for the game to start
            controller.show_frame(Page2)


# Where you wait for game to start
class Page1(tk.Frame, tkinterApp):
    def __init__(self, parent, controller, client):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        label = ttk.Label(self, text="Waiting to start", font=LARGEFONT)
        label.place(relx=.5, rely=0.05, anchor="c")

        button1 = ttk.Button(self, text="Return to start",
                             command=lambda: controller.show_frame(StartPage))
        button1.place(relx=.5, rely=0.15, anchor="c")

        meme = Image.open('progmeme.png')
        meme = ImageTk.PhotoImage(meme)
        meme_lbl = tk.Label(self, image=meme)
        meme_lbl.image = meme
        meme_lbl.place(relx=.5, rely=0.7, anchor="c")


# Host page to start the game
class hostPage(tk.Frame, tkinterApp):
    def __init__(self, parent, controller, client):
        tk.Frame.__init__(self, parent)
        self.client = client

        label = ttk.Label(self, text="", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        label = ttk.Label(self, text="Ready to start", font=LARGEFONT)
        label.place(relx=.5, rely=0.05, anchor="c")

        button1 = ttk.Button(self, text="Return to start",
                             command=lambda: controller.show_frame(StartPage))
        button1.place(relx=.5, rely=0.15, anchor="c")

        button2 = ttk.Button(self, text="Start Game",
                             command=lambda: self.fetchPage1(controller))
        button2.place(relx=.5, rely=0.22, anchor="c")

        meme = Image.open('progmeme.png')
        meme = ImageTk.PhotoImage(meme)
        meme_lbl = tk.Label(self, image=meme)
        meme_lbl.image = meme
        meme_lbl.place(relx=.5, rely=0.7, anchor="c")

    # Start game button handle
    def fetchPage1(self, controller):
        controller.show_frame(hostPlayerCount)

# Host page to start the game
class hostPlayerCount(tk.Frame, tkinterApp):
    def __init__(self, parent, controller, client):
        tk.Frame.__init__(self, parent)
        self.client = client

        label = ttk.Label(self, text="", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        label = ttk.Label(self, text="How many players are you expecting?")
        label.place(relx=.5, rely=0.05, anchor="c")

        self.PlayerCount: Entry = tk.Entry(self)
        self.PlayerCount.place(relx=.5, rely=0.1, anchor="c")

        button1 = ttk.Button(self, text="Return to start",
                             command=lambda: controller.show_frame(StartPage))
        button1.place(relx=.5, rely=0.15, anchor="c")

        button2 = ttk.Button(self, text="Submit",
                             command=lambda: self.fetchNext(controller))
        button2.place(relx=.5, rely=0.22, anchor="c")

        meme = Image.open('progmeme.png')
        meme = ImageTk.PhotoImage(meme)
        meme_lbl = tk.Label(self, image=meme)
        meme_lbl.image = meme
        meme_lbl.place(relx=.5, rely=0.7, anchor="c")

    # Start game button handle
    def fetchNext(self, controller):
        TotalPlayerCount = self.PlayerCount.get()
        # Tell server to start game
        self.client.sendMessage(key='startGameRequest', message='True')
        serverKey = self.client.listen()
        self.client.memeImage = serverKey[1]
        controller.show_frame(Page2)  # Continue to next page (page 2)


# Write funny haha meme text page
class Page2(tk.Frame):
    def __init__(self, parent, controller, client):
        tk.Frame.__init__(self, parent)
        self.client = client

        label = ttk.Label(self, text="", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        label = ttk.Label(self, text="Write a funny meme", font=LARGEFONT)
        label.place(relx=.5, rely=0.05, anchor="c")

        # Inserts the image and resizes it to fit the screen size
        meme = Image.open('images/' + self.client.memeImage)
        meme = resizeImage(meme)
        meme = ImageTk.PhotoImage(meme)

        self.meme_lbl = tk.Label(self, image=meme)
        self.meme_lbl.image = meme
        self.meme_lbl.grid(row=1, column=1, padx=10, pady=10)

        # Text box to write funny haha meme
        self.MemeText: Entry = tk.Entry(self)
        self.MemeText.grid(row=2, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Submit",
                             command=lambda: self.fetchPage2(controller))
        button2.grid(row=3, column=1, padx=10, pady=10)

    # def update(self):
    # pass

    # Submit text button handle
    def fetchPage2(self, controller):
        userInputText = self.MemeText.get()  # Get written text input to image
        assert userInputText != ""
        self.client.sendMessage('imageTextRequest', userInputText)  # Send the text input to the server

        # Let the host listen for score giving state
        serverKey = self.client.listen()
        if serverKey[0] == 'imageScoreRequest':
            imageTexts = serverKey[1]  # Get all players texts

            # Make meme for each text input into the image
            for text in imageTexts:
                print(text)
                memeImage = edit_image(self.client.memeImage, text[:1], text[2:])
                self.client.memelist.append(memeImage)

            controller.show_frame(Page3)


# Voting screen leggoooo
class Page3(tk.Frame):
    def __init__(self, parent, controller, client):
        tk.Frame.__init__(self, parent)
        self.client = client

        label = ttk.Label(self, text="", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        label = ttk.Label(self, text="---Voting Time---", font=LARGEFONT)
        label.place(relx=.5, rely=0.05, anchor="c")

        # For loop that shows funny memes, only shows equal to amount of players
        for x, meme in enumerate(self.client.memelist):
            w, h = meme.size
            print(meme)
            # Resizes images depending on the longest side
            # If horizontal - places images in a 2 x 2 grid

            # Make the 'vote' button
            button1 = ttk.Button(self, text="Vote")
            button1.value = x
            button1.configure(command=lambda button=button1: self.buttonCheck(button, controller))

            if w > h:
                scale = w / h
                w = int(500)
                h = int(w / scale)
                meme = meme.resize((w, h))
                meme = ImageTk.PhotoImage(meme)
                meme_lbl = tk.Label(self, image=meme)
                meme_lbl.image = meme

                # Makes the images go into a grid
                if int(x / 2) == 0:
                    meme_lbl.grid(row=int(x / 2 + 1), column=x % 2 + 1, padx=10, pady=10)
                if int(x / 2) == 1:
                    meme_lbl.grid(row=int(x / 2 + 2), column=x % 2 + 1, padx=10, pady=10)

                # Makes the buttons fit with the images and go below them
                if int(x / 2) == 0:
                    button1.grid(row=int(x / 2 + 2), column=x % 2 + 1, padx=10, pady=10)
                if int(x / 2) == 1:
                    button1.grid(row=int(x / 2 + 4), column=x % 2 + 1, padx=10, pady=10)

            # If vertical - places all images in a line w a button
            elif w < h:

                scale = h / w
                h = int(450)
                w = int(h / scale)
                meme = meme.resize((w, h))
                meme = ImageTk.PhotoImage(meme)
                meme_lbl = tk.Label(self, image=meme)
                meme_lbl.image = meme
                meme_lbl.grid(row=1, column=x, padx=10, pady=10)

                button1.grid(row=2, column=x, padx=10, pady=10)

    def buttonCheck(self, button, controller):
        # Score to send to server
        score = str(button.value)
        self.client.sendMessage('imageScoreRequest', score)
        serverKey = self.client.listen()

        if serverKey[0] == 'packedScores':
            self.client.packedScores = serverKey[1]
            controller.show_frame(Page4)  # Go to page 4 (Score board)

        """
            print(f'{self.client.sortedNames=}')
            if not hasattr(self.client, 'sortedPoints'):
                serverKey = self.client.listen() # Start listen again

        if serverKey[0] == 'sortedPoints':
            self.client.sortedPoints = serverKey[1]
            print(f'{self.client.sortedPoints=}')
            if not hasattr(self.client, 'sortedNames'):
                serverKey = self.client.listen() # Start listen again

        if hasattr(self.client, 'sortedNames') and hasattr(self.client, 'sortedPoints'):
            self.client.packedScores = list(zip(self.client.sortedNames, self.client.sortedPoints))
        """


# Score screen
class Page4(tk.Frame):

    def __init__(self, parent, controller, client):
        tk.Frame.__init__(self, parent)
        self.client = client

        label = ttk.Label(self, text="---SCORE---", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        print(f'{self.client.packedScores=}')

        # Displays all the names
        for x, player in enumerate(reversed(self.client.packedScores)):
            print(f'{player=}')

            label = ttk.Label(self, text=x + 1, font=LARGEFONT)
            label.grid(row=x + 1, column=0, padx=10, pady=10)

            label = ttk.Label(self, text=player[0], font=LARGEFONT)
            label.grid(row=x + 1, column=1, padx=10, pady=10)

            label = ttk.Label(self, text=player[1], font=LARGEFONT)
            label.grid(row=x + 1, column=2, padx=10, pady=10)

        button1 = ttk.Button(self, text="New Game",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(row=players + 2, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="High Scores", command=lambda: controller.show_frame(HighScorePage))
        button2.grid(row=players + 3, column=1, padx=10, pady=10)


class HighScorePage(tk.Frame):

    def __init__(self, parent, controller, client):
        tk.Frame.__init__(self, parent)
        self.client = client

        label = ttk.Label(self, text="HIGH SCORES", font=LARGEFONT)
        label.grid(row=0, column=0, padx=10, pady=10)
        scores = loadScores("allTimeHighScore.txt")
        self.showhighscore(scores)

        button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Page4))
        button1.grid(row=0, column=1, padx=10, pady=10)

    def showhighscore(self, highlist):
        for x, score in enumerate(reversed(highlist)):
            if x > 10:
                break
            label = ttk.Label(self, text=score, font=10)
            label.grid(row=x + 1, column=0, padx=10, pady=10)


# Driver Code
if __name__ == '__main__':
    tkinterApp().mainloop()
