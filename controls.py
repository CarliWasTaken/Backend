from agent import AgentMoveController

agent = AgentMoveController()

# scales the data and activates the steering servo
def steer(angle):
        angle = int((angle+127)/254*140)
        agent.servos["steering"].set_value(angle)

# scales the data and activates the throttle servo
def drive(throttle):
        print(throttle)
        throttle = int((throttle+127)/254*100)
        agent.servos["speed"].set_value(throttle)
