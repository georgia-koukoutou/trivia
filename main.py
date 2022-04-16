from game_state import GameState
from ui.main_window import MainWindow


def on_closing():

    GameState.get_instance().stop_countdown_task()
    root.destroy()


if __name__ == '__main__':

    global root
    # create main GUI
    root = MainWindow()
    root.title('Trivia')
    # clean up on close
    root.protocol("WM_DELETE_WINDOW", on_closing)
    # start event loop
    root.mainloop()




