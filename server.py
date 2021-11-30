from log.log import Log
import socket
import json
from car.controller import Controller
from car.safety import Safety
from cam.camera import Camera
import numpy as np
import time


class Server:
    # Config for the server
    _instance = None
    _localIP = "192.168.43.103"
    _localPort = 20001
    _bufferSize = 32
    _collect_training_data = True

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.log = Log.get_instance()
            cls._instance.controller = Controller.instance()
            cls._instance.camera = Camera.instance()
            cls._instance.safety = Safety.instance()
            cls._instance.images = []
            cls._instance.labels = [] # [(steer, speed)]


        return cls._instance

    # Start the server and listen for messages
    def start(self):
        # Creating and starting the server
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self._localIP, self._localPort))
        self.log.info("UDP server up and listening")
        
        # Listen for incoming datagrams
        prev_throttle = 0
        counter = 0
        while True:
            data = self.receive_data()
            # Check if data is in bounds
            if data["speed"] < -1 or data["speed"] > 1:
                # Stop the car if not
                self.controller.stop()
                prev_throttle = 0
            else:
                # Send command to steer and drive
                self.controller.steer(data['steer'])
                prev_throttle = self.controller.drive(data['speed'], prev_throttle)
                if self._collect_training_data and counter%50==0:
                    #self.camera.get_frame()
                    frame = np.array(self.camera.get_frame())
                    label = np.array((data['steer'], data['speed']))
                    #print(frame)
                    #print(label)
                    self.images.append(frame)
                    self.labels.append(label)
                    
                counter += 1


    # Close the server
    def stop(self):
        self.UDPServerSocket.close()

    # Receive and decode data
    def receive_data(self):
        bytesAddressPair = self.UDPServerSocket.recvfrom(self._bufferSize)
        message = bytesAddressPair[0]
        clientMsg = message.decode('ascii')
        clientMsg = clientMsg.replace("'", "\"")
        data = json.loads(clientMsg)

        self.safety.update_time()

        return data

if __name__ == '__main__':
    server = Server.instance()
    try:
        server.start()
    except:
        server.controller.stop()
        np.save('data/images.npy', server.images)
        np.save('data/labels.npy', server.labels)
        server.stop()
