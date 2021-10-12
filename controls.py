from adafruit_servokit import ServoKit
import time


kit = ServoKit(channels=16)

def steer(angle):
        angle = int((angle+127)/254*140)
        kit.servo[0].angle=angle

def drive(throttle):
        throttle = int((throttle+127)/254)
        kit.continuous_servo[8].throttle=throttle



def test():
    for i in range(0,180,10):
        print(i)
        kit.servo[0].angle = i
        time.sleep(0.5)
