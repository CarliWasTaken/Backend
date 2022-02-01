import sys
sys.path.append('../')

import Adafruit_PCA9685
from log.log import Log
from typing import *

log: log = Log.get_instance()

class Servo():
    def __init__(self, pwm: Adafruit_PCA9685.PCA9685, number: int, neutral: int, delta_max: int) -> None:
        self.__pwm: Adafruit_PCA9685.PCA9685 = pwm
        self.__number = number
        self.__neutral = neutral
        self.__delta_max = delta_max
        pass

    # sets the servo to its neutral value
    def set_neutral(self) -> None:
        '''Sets a servo to his neutral value

        This method is for the servo to the corresponding default value.
        '''
        self.__pwm.set_pwm(self.__number, 0, self.__neutral)
        pass

    # checks if the value is in the accepted range
    # def check_value(self, value) -> int:
    #     if value > self.__neutral + self.__delta_max:
    #         value = self.__neutral + self.__delta_max

    #     if value < self.__neutral - self.__delta_max:
    #         value = self.__neutral - self.__delta_max

    #     return value

    def set_value(self, value: int) -> None:
        '''Set give value
        
        This method is mainly for setting the throttle and the steering angle of the servos/motors

        Parameter
        ---------
        value
            corresponding value
        '''
        if(self.__number == 8):
            log.info(f"Throttle: {value}")
        self.__pwm.set_pwm(self.__number, 0, self.__neutral + value)
        pass


class AgentMoveController():
    def __init__(self):
        self.__pwm: Adafruit_PCA9685.PCA9685 = Adafruit_PCA9685.PCA9685()
        self.servos: dict = {
            "steering": Servo(self.__pwm, 0, 1200, 40),
            "speed": Servo(self.__pwm, 8, 1200, 40),
        }

        self.reset_servos()

        self.__servoMax= 100
        self.__servoMin = 0
        pass

    def reset_servos(self) -> None:
        '''Sets all servos to their neutral value
        
        This method is for resetting the servos corresponding to their default values.
        '''
        self.servos["speed"].set_neutral()
        self.servos["steering"].set_neutral()
        pass