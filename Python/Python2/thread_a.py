import threading
import time

class ThreadTest (threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        while True:
            print(f"i am in thread {self.name}")
            time.sleep(1)


if __name__ == "__main__":
    threads = []
    for i in range(4):
        t = ThreadTest(i)
        threads.append(t)
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()