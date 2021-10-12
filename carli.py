from flask import Flask, Response
from flask_socketio import SocketIO, emit
import logging
import camera

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/video')
def video_feed():
    return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Starting server")
    socketio.run(app, port=5000, host='0.0.0.0')