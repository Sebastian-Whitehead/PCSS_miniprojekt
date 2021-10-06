import tkinter as tk
from tkinter import ttk, Entry
from PIL import Image, ImageTk
from program.Client import Client

LARGEFONT = ("Verdana", 35)

players = 4
player_names = ["Rebecca", "Charlotte", "Tonko", "Tobias"]


class tkinterApp(tk.Tk, Client):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        container = tk.Frame(self, )
        container.grid()

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2, Page3, Page4):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2, page3, and page4 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Start game
class StartPage(tk.Frame, tkinterApp):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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

        # IPhjmmm
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
        self.connectToServer(IP, name)
        # Continue to page 1
        controller.show_frame(Page1)


# Where you wait for game to start
class Page1(tk.Frame, tkinterApp):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        label = ttk.Label(self, text="Venter på start", font=LARGEFONT)
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

        # Continue to next page (page 2)
        controller.show_frame(Page2)


# Write funny haha meme text page
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        label = ttk.Label(self, text="Write a funny harald meme", font=LARGEFONT)
        label.place(relx=.5, rely=0.05, anchor="c")

        # Inserts the image and resizes it to fit the screen size
        meme = Image.open('work.jpg')
        w, h = meme.size
        if w > h:
            scale = w / h
            w = int(500)
            h = int(w / scale)
        elif w < h:
            scale = h / w
            h = int(450)
            w = int(h / scale)
        meme = meme.resize((w, h))
        meme = ImageTk.PhotoImage(meme)
        meme_lbl = tk.Label(self, image=meme)
        meme_lbl.image = meme
        meme_lbl.grid(row=1, column=1, padx=10, pady=10)

        # Text box to write funny haha meme
        self.MemeText: Entry = tk.Entry(self)
        self.MemeText.grid(row=2, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Submit",
                             command=lambda: self.fetchPage2(controller))
        button2.grid(row=3, column=1, padx=10, pady=10)

    # Submit text button handle
    def fetchPage2(self, controller):
        # Get written text input to image
        userInputText = self.MemeText.get()

        # Continue to next page (Voting page)
        controller.show_frame(Page3),

    # Voting screen leggoooo


class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        label = ttk.Label(self, text="---Voting Time---", font=LARGEFONT)
        label.place(relx=.5, rely=0.05, anchor="c")

        memelist = ('andreas.png','andreas.png','andreas.png','andreas.png')
        buttonlist = ()
        # For loop that shows funny memes, only shows equal to amount of players
        for x in range(players):
            meme = Image.open(memelist[x])
            w, h = meme.size
            # Resizes images depending on the longest side
            # If horizontal - places images in a 2 x 2 grid
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

                button1 = ttk.Button(self, text="Yass this queen",
                                     command=lambda: controller.show_frame(Page4))

                # Makes the buttons fit with the images and go below them
                if int(x / 2) == 0:
                    button1.grid(row=int(x / 2 + 2), column=x % 2 + 1, padx=10, pady=10)
                if int(x / 2) == 1:
                    button1.grid(row=int(x / 2 + 4), column=x % 2 + 1, padx=10, pady=10)
                buttonlist.append(button1)
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

                button1 = ttk.Button(self, text="Yass this queen",
                                     command=lambda: controller.show_frame(Page4))
                button1.grid(row=2, column=x, padx=10, pady=10)
                buttonlist.append(button1)



# Score screen
class Page4(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="---SCORE---", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        # Displays all the names
        for x in range(players):
            label = ttk.Label(self, text=x + 1, font=LARGEFONT)
            label.grid(row=x + 1, column=0, padx=10, pady=10)

            label = ttk.Label(self, text=player_names[x], font=LARGEFONT)
            label.grid(row=x + 1, column=1, padx=10, pady=10)

        button1 = ttk.Button(self, text="m'ka' goodnight",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(row=players + 2, column=1, padx=10, pady=10)


# Driver Code
app = tkinterApp()
app.mainloop()
