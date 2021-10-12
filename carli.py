import Adafruit_PCA9685

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

        self.__pwm = Adafruit_PCA9685.PCA9685()
        self.servos = {
            "steering": Servo(self.__pwm, 0, 335, 40),
            "speed": Servo(self.__pwm, 8, 370, 80),
        }

        self.reset_servos()

        self.__servoMax = 100
        self.__servoMin = 0
        pass

    def __del__(self):
        self.reset_servos()
        pass

    def reset_servos(self):
        self.servos["speed"].set_neutral()
        self.servos["steering"].set_neutral()
        pass


    def scaleData(self, dataSet):
        return self.__servoMin + dataSet * (self.__servoMax - self.__servoMin)
        pass


if __name__ == '__main__':
    demo = AgendMoveController()
    while True:
        demo.servos["speed"].set_value(30)
        demo.servos["steering"].set_value(1)
