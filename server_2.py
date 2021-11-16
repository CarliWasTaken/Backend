from log import Log
import socket
import json
import time
from threading import Thread
import cv2
import numpy as np
from safety import Safety

time_last_message = time.time()

'''def generate_data_point(camera, steer, speed):
    success, frame = camera.read()
    if success:
        frame = np.array(frame)
        print(frame.shape)'''

          

log = Log.get_instance()

localIP = "192.168.43.103"
localPort = 20001
bufferSize = 32

camera = cv2.VideoCapture(0)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

log.info("UDP server up and listening")

# Listen for incoming datagrams

try:
    safety = Safety()
    prev_throttle = 0
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        clientMsg = message.decode('ascii')
        clientMsg = clientMsg.replace("'", "\"")
        data = json.loads(clientMsg)
    
        # Log the movement data
        #log.move(data['speed'], data['steer'])
    
        # Set currrent time as time of last message
        safety.update_time()

        if data["speed"] < -1 or data["speed"] > 1:
            controls.stop()
            prev_throttle = 0
        else:
            controls.steer(data['steer'])
            prev_throttle = controls.drive(data['speed'], prev_throttle)


except Exception as ex:
    print(str(ex))
    controls.stop()