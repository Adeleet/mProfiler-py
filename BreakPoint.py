from time import time


class BreakPoint:
    def __init__(self):
        self.start_time = time()

    def end(self):
        self.end_time = time()

    def get_start(self):
        return self.start_time
    
    def get_end(self):
        if not hasattr(self,)