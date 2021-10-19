from log import Log
import socket
import json
import controls

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

    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]

        clientMsg = message.decode('ascii')
        clientMsg = clientMsg.replace("'", "\"")
        data = json.loads(clientMsg)
    
        # Log the movement data
        #log.move(data['speed'], data['steer'])
    
        controls.steer(data['steer'])
        controls.drive(data['speed'])

except KeyboardInterrupt:
    controls.drive(0)

controls.drive(0)
