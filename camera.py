import cv2

def gen_frames(camera):
    # read camera frame
    success, frame = camera.read() 
    print(frame)
    if success:
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        return (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 


def stream():
    camera = cv2.VideoCapture(0)
    while True:
        yield gen_frames(camera)

if __name__ == '__main__':
    