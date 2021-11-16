import time
from threading import Thread
from controller import Controller
from typing import *

class Safety(Thread):
    '''Creates safety that checks how long ago last message was and stops if necessary'''

    _instance :Safety = None

    @classmethod
    def instance():
        '''returns the instance of the class'''
        if Safety._instance == None:
            Safety._instance = Safety()
        return Safety._instance

    def __init__(self, controller :Controller):
        Thread.__init__(self)
        self.controller :Controller = controller

        self.daemon = True
        self.start() # starts the `run()` method
        self.time_last_message :float = time.time()

    def run(self):
        while True:
            if time.time() - self.time_last_message > 0.5: # stop if last message is longer than 0.5 seconds ago
                self.controller.stop()
            time.sleep(0.5)

    def update_time(self):
        '''updates the timestamp of the last message'''
        self.time_last_message = time.time()