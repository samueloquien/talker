import time
import sys

class ElapsedTimer:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.start_time = time.time()
    
    def report(self,txt=''):
        t = time.time()
        elapsed = t-self.start_time
        self.start_time = t
        print(f'{txt} - elapsed: {elapsed:.03f}s')

