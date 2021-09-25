from flask import Flask, Response, request
from flask_socketio import SocketIO, emit
import logging
import controls
from camera import Camera

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
streaming = False

@socketio.on('forward', namespace='/drive')
def handle_forward(data):
    controls.forward(data)

@socketio.on('backward', namespace='/drive')
def handle_backward(data):
    controls.backward(data)

@socketio.on('left', namespace='/drive')
def handle_left(data):
    controls.left(data)

@socketio.on('right', namespace='/drive')
def handle_right(data):
    controls.right(data)

# On client connect fire this message
@socketio.on('connect', namespace='/stream')
def handle_stream_connect():
    # Sends a test message to the user when connecting
    emit('ai', 'Test1')
    pass

# Should deactivate the while loop is client disconnects (doesn't work or does it?)
@socketio.on('disconnect', namespace='/stream')
def handle_stream_disconnect():
    global streaming
    streaming = False
    print('Streaming ended!')
    pass

# Starts the stream to the user
@socketio.on('start_stream', namespace='/stream')
def handle_start_stream(data):
    global streaming
    streaming = True
    print('Starting streaming...')
    stream()

# Streaming function for the video
def stream():
    # create Camera with the cameraId
    c = Camera(1)
    global streaming
    while streaming:
        # captures an image
        c.capture_frame()
        # send picture bytes to the user
        emit('video', c.get_bytes())
        c.create_ai_image()
        emit('ai', c.get_bytes())
        
if __name__ == '__main__':
    print("Starting server")
    socketio.run(app, port=5000, host='0.0.0.0')