import Adafruit_PCA9685
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)

class Servo():
    def __init__(self, pwm, number, neutral, delta_max):
        self.__pwm = pwm
        self.__number = number
        self.__neutral = neutral
        self.__delta_max = delta_max
        self.__current_value = 0
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
        
        self.__pwm = Adafruit_PCA9685.PCA9685(i2c)
        print(self.__pwm)
        self.servos = {
            "speed": Servo(pwm, 8, 335, 40),
            "steering": Servo(pwm, 0, 370, 80),
            #"camera": Servo(pwm, 3, 370, 130),
        }
        
        #self.reset_servos()
        
        self.__servoMax = 100
        self.__servoMin = 0
        
        #self.server = UgvServer(self.setServos)
        pass
    
    def __del__(self):
        self.reset_servos();
        pass
    
    def reset_servos(self):
        print(self.servos)
        self.servos["speed"].set_neutral()
        self.servos["steering"].set_neutral()
        pass
    
    def setServos(self, data):
        print('callback called')
        datagram = str(data).split(';')
        for i in range(len(datagram)):
            if i == 1:
                self.servos["speed"].set_value(datagram[i])
                pass
            if i == 2:
                self.servos["steering"].set_value(datagram[i])
                pass
            
        pass
        
    def scaleData(self, dataSet):
        return self.__servoMin + dataSet * (self.__servoMax - self.__servoMin)
        pass
    
    #def start(self):
     #   self.server.start_server()
      #  pass

if __name__ == '__main__':
    demo = AgendMoveController()
    demo.servos["steering"].set_value(1)
