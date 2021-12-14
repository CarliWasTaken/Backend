from cam.camera import Camera
import numpy as np
import cv2


c = Camera.instance()

frame = np.array(c.get_frame())
frame = cv2.resize(frame, (0,0), fx=0.1, fy=0.1)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


print(frame.shape)
