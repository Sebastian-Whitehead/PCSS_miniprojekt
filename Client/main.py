import tkinter as tk
from tkinter import ttk, Entry
from PIL import Image, ImageTk
from Client import Client
from edit_image import edit_image, resizeImage
from handleHighScoreList import *
import Bubble_sort

LARGEFONT = ("Verdana", 35)

players = 4
player_names = ["Rebecca", "Charlotte", "Tonko", "Tobias"]


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

        label = ttk.Label(self, text="Navn hmm?")
        label.grid(row=1, column=0, padx=10, pady=10)

        # Name of player
        self.PName: Entry = tk.Entry(self)
        self.PName.grid(row=2, column=0, padx=10, pady=10)

        label = ttk.Label(self, text="IP hmm?")
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
        # Get written name in name input
        name = self.PName.get()
        # Get written IP in IP input
        # (Does not do anything at the moment)
        IP = self.IPName.get()
        # Connect to server with name and IP
        self.client.connectToServer(IP, name)
        # Continue to page 1
        controller.show_frame(Page1)

        # Listen for server
        serverKey = self.client.listen()
        # Let the host listen for game start request
        if serverKey[0] == 'startGameRequest':
            controller.show_frame(hostPage)
        # Let all other players wait for the game to start
        elif serverKey[0] == 'imageTextRequest':
            controller.show_frame(Page2)


# Where you wait for game to start
class Page1(tk.Frame, tkinterApp):
    def __init__(self, parent, controller, client):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        label = ttk.Label(self, text="Venter på start", font=LARGEFONT)
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
        print('Starting game')
        # Tell server to start game
        self.client.sendMessage(key='startGameRequest', message='True')
        serverKey = self.client.listen()
        self.client.memeImage = serverKey[1]
        # Continue to next page (page 2)
        controller.show_frame(Page2)


# Write funny haha meme text page
class Page2(tk.Frame):
    def __init__(self, parent, controller, client):
        tk.Frame.__init__(self, parent)
        self.client = client

        label = ttk.Label(self, text="", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        label = ttk.Label(self, text="Write a funny harald meme", font=LARGEFONT)
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
        # Get written text input to image
        userInputText = self.MemeText.get()
        # Send the text input to the server
        self.client.sendMessage('imageTextRequest', userInputText)

        # Let the host listen for score giving state
        # EKSTRA LISTEN DON NO WHY Can maybe be deleted
        # serverKey = self.client.listen()
        # print(serverKey)
        serverKey = self.client.listen()
        if serverKey[0] == 'imageScoreRequest':
            # Get all players texts
            imageTexts = serverKey[1]
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
            button1 = ttk.Button(self, text="Yass queen " + str(x))
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
        if serverKey[0] == 'winnerChickenDinner':
            self.client.points = serverKey[1]
            # Go to page 4 (Score board)
            controller.show_frame(Page4)


# Score screen


class Page4(tk.Frame):

    def __init__(self, parent, controller, client):
        tk.Frame.__init__(self, parent)
        self.client = client

        label = ttk.Label(self, text="---SCORE---", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        # Handling score
        print('Handling score..')
        print(f'{self.client.points=}')
        countedPoints = Bubble_sort.countPoints(self.client.points, len(self.client.points))
        print(f'{countedPoints=}')
        sortedPoints = Bubble_sort.bubble_sort(countedPoints)
        print(f'{sortedPoints=}')

        ''' Get the winner
        winnerValue = max(countedPoints)
        winnerIndex = countedPoints.index(winnerValue)
        winner = 'Player ' + str(winnerIndex)
        print('Winner is', winner)
        print('')
        '''

        # Displays all the names
        for x, score in enumerate(sortedPoints):
            label = ttk.Label(self, text=x + 1, font=LARGEFONT)
            label.grid(row=x + 1, column=0, padx=10, pady=10)

            label = ttk.Label(self, text=player_names[x], font=LARGEFONT)
            label.grid(row=x + 1, column=1, padx=10, pady=10)

        button1 = ttk.Button(self, text="m'ka' goodnight",
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
