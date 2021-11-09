import Adafruit_PCA9685
from log import Log

log = Log.get_instance()

class Servo():
    def __init__(self, pwm, number, neutral, delta_max):
        self.__pwm = pwm
        self.__number = number
        self.__neutral = neutral
        self.__delta_max = delta_max
        pass

    def __del__(self):
        self.set_neutral()
        pass

    # sets the servo to its neutral value
    def set_neutral(self):
        log.info('Neutral')
        self.__pwm.set_pwm(self.__number, 0, self.__neutral)
        pass

    # checks if the value is in the accepted range
    def check_value(self, value):
        if value > self.__neutral + self.__delta_max:
            value = self.__neutral + self.__delta_max

        if value < self.__neutral - self.__delta_max:
            value = self.__neutral - self.__delta_max

        return value

    # sets the servo to a specific value
    def set_value(self, value):
        #log.info(str(self.__number)  + ': ' + str(self.__neutral + value))
        self.__pwm.set_pwm(self.__number, 0, self.__neutral + value)
        pass


class AgentMoveController():
    def __init__(self):
        self.__pwm = Adafruit_PCA9685.PCA9685()
        self.servos = {
            "steering": Servo(self.__pwm, 0, 1200, 40),
            "speed": Servo(self.__pwm, 8, 1200, 40),
        }

        self.reset_servos()

        self.__servoMax = 100
        self.__servoMin = 0
        pass

    def __del__(self):
        self.reset_servos()
        pass

    # resets the Servos
    def reset_servos(self):
        self.servos["speed"].set_neutral()
        self.servos["steering"].set_neutral()
        pass

    # scales the data
    def scaleData(self, dataSet):
        return self.__servoMin + dataSet * (self.__servoMax - self.__servoMin)
