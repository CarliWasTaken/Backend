from log.log import Log
import socket
import json
from car.controller import Controller
from car.safety import Safety
from cam.camera import Camera
from datetime import datetime
import os
import cv2
from nn.custom_neural_network import CustomNeuralNetwork

class Server:
    # Config for the server
    _instance = None
    _localIP = "192.168.43.103"
    #_localIP = "127.0.0.1"
    _localPort = 20001
    _bufferSize = 32
    _collect_training_data = True
    # Higher is less often
    _collect_training_data_freq = 10

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
            d = now.strftime("%Y%m%dT%H%M%S")

            path = f'{os.getcwd()}{os.sep}data{os.sep}{d}{os.sep}'
            os.mkdir(path)
        
        prev_throttle = 0
        counter = 0

        # Listen for incoming datagrams
        while True:
            data = self.receive_data()

            # Check if data is in bounds
            # AI mode
            if data["speed"] == 123:
                frame = self.camera.get_frame()
                speed = 0.18
                steer = self.nn.query(frame)[0][0]
                steer = (steer-0.5)*2
                self.controller.steer(steer)
                prev_throttle = self.controller.drive(speed, prev_throttle)
                continue

            elif -1 <= data["speed"] <= 1:
                # Send command to steer and drive
                self.controller.steer(data['steer'])
                prev_throttle = self.controller.drive(data['speed'], prev_throttle)

                if self._collect_training_data and counter%self._collect_training_data_freq==0:
                    frame = self.camera.get_frame()
                    label = data['steer']
                    im_path = path+f"{counter/self._collect_training_data_freq}_{label}.jpg"
                    print(im_path)
                    cv2.imwrite(im_path, frame)

            else:
                # Stop the car if not
                self.controller.stop()
                prev_throttle = 0
                    
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
        server.controller.stop()
        server.stop()
        server.log.error(e)
