import socket
import json
import controls

localIP = "192.168.43.25"
localPort = 20001
bufferSize = 32

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]

    clientMsg = message.decode('ascii')
    clientMsg = clientMsg.replace("'", "\"")
    data = json.loads(clientMsg)
    #print(data)
    
    controls.steer(data['steer'])
    #controls.drive(data['speed'])
