from agent import AgentMoveController
import time
from log import Log

agent = AgentMoveController()
log = Log.get_instance()

#practically acceleration, lower is slower
max_throttle_increment = 0.01


# scales the data and activates the steering servo
def steer(angle):
        angle = int(300*angle)
        agent.servos["steering"].set_value(angle)

# scales the data and activates the throttle servo
def drive(throttle, prev_throttle):
    if throttle >= 0:
        throttle = min(prev_throttle+max_throttle_increment, throttle)
    else:
        throttle = max(prev_throttle-max_throttle_increment, throttle)

    prev_throttle = throttle
    throttle = int(400*throttle)
    agent.servos["speed"].set_value(throttle)
    return prev_throttle

# Stops the motor and resets steering
def stop():
    agent.servos["speed"].set_value(0)
    agent.servos["steering"].set_value(0)