from flask import Flask, Response
import cv2
import numpy as np
from flask_socketio import SocketIO
import controls

app = Flask(__name__)

socketio = SocketIO(app)

if __name__ == '__main__':
    print("Starting server")
    socketio.run(app)

@socketio.on('forward')
def handle_message(data):
    controls.forward(data)

@socketio.on('backward')
def handle_message(data):
    controls.backward(data)

@socketio.on('steer')
def handle_message(data):
    controls.steer(data)