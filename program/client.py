# https://www.tutorialspoint.com/python/python_networking.htm
import socket, pickle       # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 1024                 # Reserve a port for your service.

s.connect((host, port))
print(s.recv(1024).decode("utf-8"))
while True:
    print('Hi! What is your name?')
    name = (input('Type your name here: ').encode(), 'name')
    s.send(pickle.dumps(name))
s.close()
