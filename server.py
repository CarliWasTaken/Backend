from log import Log
import socket
import json
import controls
import time
from threading import Thread

time_last_message = time.time()

class Safety(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            if time.time() - time_last_message > 0.5:
                controls.stop()
            time.sleep(0.5)
            

log = Log.get_instance()

localIP = "192.168.43.103"
localPort = 20001
bufferSize = 32


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

log.info("UDP server up and listening")

# Listen for incoming datagrams

try:
    Safety()
    prev_throttle = 0
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        clientMsg = message.decode('ascii')
        clientMsg = clientMsg.replace("'", "\"")
        data = json.loads(clientMsg)
    
        # Log the movement data
        #log.move(data['speed'], data['steer'])
    
        time_last_message = time.time() 
        if data["speed"] < -1 or data["speed"] > 1:
            controls.stop()
        else:
            controls.steer(data['steer'])
            #log.info(data["speed"])
            prev_throttle = controls.drive(data['speed'], prev_throttle)

except Exception as ex:
    print(str(ex))
    controls.stop()


