from flask import Flask, Response
from flask_socketio import SocketIO, emit
import logging
import controls
import camera

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


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

@app.route('/video')
def video_feed():
    return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Starting server")
    socketio.run(app, port=5000, host='0.0.0.0')