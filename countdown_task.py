import time
from threading import Thread
from tkinter import IntVar


class CountdownTask(Thread):

    def __init__(self, counter: IntVar):
        super().__init__()

        self.counter: IntVar = counter
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while self._running and self.counter.get() > 0:
            self.counter.set(self.counter.get() - 1)
            time.sleep(1)
