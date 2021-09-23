import cv2
import io
import socket
import struct
import time
import pickle
import zlib

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('87.72.205.154', 8485))
connection = client_socket.makefile('wb')

img_counter = 0

frame = cv2.imread("test.jpg")
data = pickle.dumps(frame, 0)
size = len(data)


print("{}: {}".format(img_counter, size))
client_socket.sendall(struct.pack(">L", size) + data)
img_counter += 1