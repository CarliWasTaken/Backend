from board import SCL, SDA
import busio
i2c = busio.I2C(SCL, SDA)
from adafruit_pca9685 import PCA9685

class Servo():
    def __init__(self, pwm, number, neutral, delta_max):
        self.__pwm = pwm
        self.__number = number
        self.__neutral = neutral
        self.__delta_max = delta_max
        int: self.__current_value = 0
        pass 
    
    def __del__(self):
        self.set_neutral()
        pass
        
        
    def set_neutral(self):
        self.__pwm.set_pwm(self.__number, 0, self.__neutral)
        pass
        
    def check_value(self, value):
        if value > self.__neutral + self.__delta_max:
            value = self.__neutral + self.__delta_max
        
        if value < self.__neutral - self.__delta_max:
            value = self.__neutral - self.__delta_max
        
        return value
        pass
    
    def set_value(self, value):
        
        self.__pwm.set_pwm(self.__number, 0, self.__neutral + value)
        pass
        

class AgendMoveController():
    def __init__(self):
        self.__pwm = PCA9685(i2c)
        self.__servos = {
            "speed": Servo(self.__pwm, 0, 335, 40),
            "steering": Servo(self.__pwm, 1, 370, 80),
        }
        
        self.reset_servos()
        
        self.__servoMax = 100
        self.__servoMin = 0
        
        self.server = UgvServer(self.setServos)
        pass
    
    def __del__(self):
        self.reset_servos()
        pass
    
    def reset_servos(self):
        self.__servos["speed"].set_neutral()
        self.__servos["steering"].set_neutral()
        pass


if __name__ == '__main__':
    demo = AgendMoveController()
    demo.__servos["speed"].set_value(10)
