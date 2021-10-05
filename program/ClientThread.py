import threading

class ClientThread(threading.Thread):
    def __init__(self):
        super(ClientThread, self).__init__()

    def run(self):
        print (self.getName())

    def setTarget(self, target):
        self.target = target

    def run(self):
        print(self.socket)