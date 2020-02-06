from process_b import Test
import time

if __name__ == "__main__":
    t = Test()
    t.start()
    while True:
        print("process a run")
        time.sleep(1)

