import sys
sys.path.append('../')

from car.agent import AgentMoveController
#from car.dev_agent import AgentMoveController
from log.log import Log
from typing import *
import time

class Controller:
    _instance = None

    # practically acceleration, lower is slower
    _max_throttle_increment: float = 1

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.agent = AgentMoveController()
            cls._instance.log = Log.get_instance()
        return cls._instance

    # scales the data and activates the steering servo
    def steer(self, angle: float) -> None:
        #self.log.info(f"Steering: {angle}")
        angle: int = int(300*angle)
        self.agent.servos["steering"].set_value(angle)
        pass

    # scales the data and activates the throttle servo
    def drive(self, throttle: float, prev_throttle: float, record: bool = False) -> float:
        #self.log.info(f"Throttle: {throttle}")
        if throttle >= 0:
            throttle = min(prev_throttle+self._max_throttle_increment, throttle)
        else:
            throttle = max(prev_throttle-self._max_throttle_increment, throttle)

        prev_throttle = throttle
        throttle: int = int(400*throttle)
        self.agent.servos["speed"].set_value(throttle)
        return prev_throttle

    # Stops the motor and resets steering
    def stop(self) -> None:
        self.agent.servos["speed"].set_value(0)
        self.agent.servos["steering"].set_value(0)
        pass