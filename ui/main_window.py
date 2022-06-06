import tkinter
from tkinter import BOTH

from ui.game_page import GamePage
from ui.landing_page import LandingPage


class MainWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self._frame = None
        self.title('Trivia')
        self.geometry('640x480')
        self.resizable(True, True)

        self.go_to_landing_page()

    def switch_frame(self, frame_class):
        # Destroys current frame and replaces it with a new one.
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=BOTH, expand=True)

    def go_to_landing_page(self):
        self.switch_frame(LandingPage)

    def go_to_game_page(self):
        self.switch_frame(GamePage)
