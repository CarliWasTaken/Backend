import sys
sys.path.append('../')

from log.log import Log
from typing import *

log = Log.get_instance()

class Servo():
    def __init__(self) -> None:
        pass

    # sets the servo to its neutral value
    def set_neutral(self) -> None:
        pass

    def set_value(self, value: int) -> None:
        pass


class AgentMoveController():
    def __init__(self):
        self.servos: dict = {
            "steering": Servo(),
            "speed": Servo(),
        }

        self.reset_servos()
        pass

    def reset_servos(self) -> None:
        self.servos["speed"].set_neutral()
        self.servos["steering"].set_neutral()
        pass