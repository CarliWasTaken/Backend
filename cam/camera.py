import cv2
import time
import numpy as np
import matplotlib as mpl

class Camera:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.cam = cv2.VideoCapture(0)

        return cls._instance

    def get_frame(self):
        ret, frame = self.cam.read()

        frame = cv2.resize(frame, (0,0), fx=0.1, fy=0.1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame =  frame[frame.shape[0]//3:, :]
        frame = cv2.Canny(frame, 50, 70)
        
        frame = frame.flatten()
        return frame

    def __del__(self):
        self.cam.release()

if __name__ == "__main__":
    cam = Camera.instance()
    while True:
        frame = cam.get_frame()
        #show frame
        print(frame.shape)
        cv2.imshow("frame", frame)
        cv2.waitKey(1)


    
