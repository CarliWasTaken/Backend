import cv2

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
        return frame

    def __del__(self):
        self.cam.release()

    