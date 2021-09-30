import cv2
import struct
import pickle
from datetime import datetime
import time
import threading

class SendReceiveImage:

    def sendImage(self, frame, sendTo):
        print('Sending image..')
        connection = sendTo.makefile('wb')

        img_counter = 0
        # while img_counter:
        data = pickle.dumps(frame, 0)
        size = len(data)

        print("{}: {}".format(img_counter, size))
        sendTo.sendall(struct.pack(">L", size) + data)
        print('img_counter:', str(img_counter), 'Size:', str(size), 'Data:', str(len(data)))
        img_counter += 1

        print('Image send,', datetime.now())
        print('')

        return True

    def receiveImage(self, c):
        print('Receiving image..')
        data = b""
        payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(payload_size))
        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data += c.recv(4096)

        print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += c.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        print('Image received,', datetime.now())
        print('')

        return frame_data
