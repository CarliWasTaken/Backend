from Agent import AgentMoveController
import time
from log import Log

agent = AgentMoveController()
log = Log.get_instance()

# scales the data and activates the steering servo
def steer(angle):
        angle = int(300*angle)
        agent.servos["steering"].set_value(angle)

# scales the data and activates the throttle servo
def drive(throttle):
    throttle = int(400*throttle)
    agent.servos["speed"].set_value(throttle)
    log.info(str(throttle))


if __name__ == '__main__':
    for i in range(-60, 60, 10):
        print(str(i))
        agent.servos["steering"].set_value(i)
        time.sleep(0.5)
