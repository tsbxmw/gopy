import time
from multiprocessing import Process

class Test(Process):
    def __init__(self):
        super().__init__()
    
    def run(self):
        while True:
            print("process b is run")
            time.sleep(1)