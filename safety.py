import time
from threading import Thread

class Safety(Thread):
    '''Creates safety that checks how long ago last message was and stops if necessary'''

    def __init__(self, controls):
        Thread.__init__(self)
        self.daemon = True
        self.start() # starts the `run()` method
        self.time_last_message = time.time()

        self.controls = controls

    def run(self):
        while True:
            if time.time() - self.time_last_message > 0.5: # stop if last message is longer than 0.5 seconds ago
                self.controls.stop()
            time.sleep(0.5)

    def update_time(self):
        '''updates the timestamp of the last message'''
        self.time_last_message = time.time()