from Agent import AgentMoveController

agent = AgentMoveController()

def steer(angle):
        angle = int((angle+127)/254*140)
        demo.servos["steering"].set_value(angle)

def drive(throttle):
        throttle = int((throttle+127)/254)
        demo.servos["speed"].set_value(throttle)