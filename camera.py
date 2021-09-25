import cv2
import numpy as np

class Camera:
    def __init__(self, camera):
        self.camera = cv2.VideoCapture(camera)

    def capture_frame(self):
        success, self.frame = self.camera.read()

    def create_ai_image(self):
        self.frame = cv2.addWeighted(self.frame, 5, np.zeros(self.frame.shape, self.frame.dtype), 0, 0)

    def get_bytes(self):
        return cv2.imencode('.jpg', self.frame)[1].tobytes()

def capture_video():
    pass

def gen_ai_frames():
    c = Camera(1)
    while True:
        c.capture_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + c.get_bytes() + b'\r\n') 
        print(c.get_bytes())

def gen_frames():
    camera = cv2.VideoCapture(1)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 