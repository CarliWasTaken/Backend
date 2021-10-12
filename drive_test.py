import controls
import time

print('Loading')

while True:
    angle = int(input('Enter speed: '))
    controls.drive(angle)



'''
for angle in range(-127,127, 30):
    controls.steer(angle)
    time.sleep(0.5)
'''


'''
controls.steer(0)
time.sleep(2)


controls.steer(64)
time.sleep(2)

controls.steer(127)
time.sleep(2)
'''
controls.steer(0)
