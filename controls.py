from Agent import AgentMoveController

agent = AgentMoveController()

def steer(angle):
        angle = int((angle+127)/254*140)
        agent.servos["steering"].set_value(angle)

def drive(throttle):
        print(throttle)
        throttle = int((throttle+127)/254*100)
        agent.servos["speed"].set_value(throttle)
