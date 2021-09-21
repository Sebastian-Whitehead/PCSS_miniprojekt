# https://www.tutorialspoint.com/python/python_networking.htm
import socket, pickle               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 1024                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print(s)
print('Running')

players = {}

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print('Got connection from:', addr)
   try:
      c.send(b'Thank you for connecting')
   except TypeError:
      print('TypeError')

      recive = c.recv(1024)
      message = pickle.loads(recive)
      print('Client sent:', repr(message))
c.close()
