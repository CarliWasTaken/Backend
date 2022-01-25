from log.log import Log
import socket
import json
from car.controller import Controller
from car.safety import Safety
from cam.camera import Camera
import numpy as np
import time
from datetime import datetime
import os
import cv2
from nn.custom_neural_network import CustomNeuralNetwork

class Server:
    # Config for the server
    _instance = None
    #_localIP = "192.168.43.103"
    _localIP = "127.0.0.1"
    _localPort = 20001
    _bufferSize = 32
    _collect_training_data = False

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
            cls._instance.labels = []
            cls._instance.nn = CustomNeuralNetwork.import_neural_net("nn/network_data/neuralnet.npy")


        return cls._instance

    # Start the server and listen for messages
    def start(self):
        # Creating and starting the server
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self._localIP, self._localPort))
        self.log.info("UDP server up and listening")
        path = None
        if self._collect_training_data:
            self.log.info("Collecting training data")
            now = datetime.now()
            d = now.strftime("%m-%d-%YT%H:%M:%S")
            path = f"/home/pi/Backend/data/{d}/"
            os.mkdir(path)
        
        # Listen for incoming datagrams
        prev_throttle = 0
        counter = 0
        while True:
            data = self.receive_data()
            # Check if data is in bounds
            if data["speed"] == 123:
                frame = self.camera.get_frame()
                speed = 0.3
                steer = self.nn.query(frame)[0][0]
                self.controller.steer(steer)
                prev_throttle = self.controller.drive(speed, prev_throttle)
                continue

            elif data["speed"] < -1 or data["speed"] > 1:
                # Stop the car if not
                self.controller.stop()
                prev_throttle = 0
            else:
                # Send command to steer and drive
                self.controller.steer(data['steer'])
                prev_throttle = self.controller.drive(data['speed'], prev_throttle)
                if self._collect_training_data and counter%10==0:
                    frame = self.camera.get_frame()
                    label = data['steer']
                    dt = datetime.now()
                    im_path = path+f"{dt}_{label}.jpg"
                    print(im_path)
                    cv2.imwrite(im_path, frame)
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
    except Exception as e:
        print(e)
        server.controller.stop()
        server.stop()
