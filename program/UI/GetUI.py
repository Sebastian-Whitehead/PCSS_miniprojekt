from main import tkinterApp
from main import StartPage
from main import Page1
from main import Page2
from program.Client import Client

class AHoldeNewClaaaas(tkinterApp, Client):
    def __init__(self):
        super().__init__()
        self.mainloop()

        #self.tkinerApp.show_frame(self.page1)




aHoldeNewClaaaas = AHoldeNewClaaaas()
"""
Client.connectToServer(ip, name)
page1 = Page1
print(page1)
print(page1.getTe)
page2 = Page2
print(page2)
"""