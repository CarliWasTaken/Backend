from flask import Flask, Response
import cv2
#import server

app = Flask(__name__)

def gen_frames(camera):
    # read camera frame
    success, frame = camera.read() 
    if success:
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        return (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 


def stream():
    camera = cv2.VideoCapture(0)
    while True:
        yield gen_frames(camera)
    

@app.route('/video')
def video_feed():
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()