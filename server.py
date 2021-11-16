from log import Log
import socket
import json
from controller import Controller
from safety import Safety
from camera import Camera


class Server:
    # Config for the server
    _instance = None
    _localIP = "192.168.43.103"
    _localPort = 20001
    _bufferSize = 32

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

        return cls._instance

    # Start the server and listen for messages
    def start(self):
        # Creating and starting the server
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((_localIP, _localPort))
        log.info("UDP server up and listening")
        
        # Listen for incoming datagrams
        try:
            prev_throttle = 0
            while True:
                data = self.receive_data()
                # Check if data is in bounds
                if data["speed"] < -1 or data["speed"] > 1:
                    # Stop the car if not
                    controls.stop()
                    prev_throttle = 0
                else:
                    # Send command to steer and drive
                    #controls.steer(data['steer'])
                    #prev_throttle = controls.drive(data['speed'], prev_throttle)
                    pass
        except Exception as ex:
            print(str(ex))
            controls.stop()

    # Close the server
    def stop(self):
        self.UDPServerSocket.close()

    # Receive and decode data
    def receive_data(self):
        bytesAddressPair = self.UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        clientMsg = message.decode('ascii')
        clientMsg = clientMsg.replace("'", "\"")
        data = json.loads(clientMsg)

        self.safety.update_time()

        return data

if __name__ == '__main__':
    server = Server.instance()
    server.start()
