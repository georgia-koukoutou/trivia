import tkinter
from tkinter import NO, CENTER, SW, SE, messagebox, YES
from tkinter.ttk import Treeview
import constants
import highscore_client
from game_state import GameState


class LandingPage(tkinter.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        category_names = GameState.get_instance().get_categories_names()
    
        self.config(padx=20, pady=10, bg=constants.BACKGROUND_COLOR)
        # setup the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(2, weight=1)

        tkinter.Label(self, text='Welcome to Trivia!', font=('Arial', 20), fg=constants.THEME_COLOR, bg=constants.BACKGROUND_COLOR) \
            .grid(row=0, column=0, columnspan=2)

        tkinter.Label(self, text='Current Leaderboard:', bg=constants.BACKGROUND_COLOR)\
            .grid(row=1, column=0, columnspan=1, sticky='w')

        self.render_table()

        username_container = tkinter.Frame(self)
        username_container.grid(row=3, column=0, columnspan=2, pady=10)

        tkinter.Label(username_container, text='Enter your name:', bg=constants.BACKGROUND_COLOR).pack(side='left')
        tkinter.Entry(username_container, textvariable=GameState.get_instance().username, highlightthickness=0).pack(side='right')

        difficulty_container = tkinter.Frame(self, background=constants.BACKGROUND_COLOR)
        difficulty_container.grid(row=4, column=0, columnspan=1)

        tkinter.Label(difficulty_container, text='Select difficulty:', bg=constants.BACKGROUND_COLOR).pack(side='left')
        sd = tkinter.OptionMenu(difficulty_container, GameState.get_instance().difficulty, None, *constants.DIFFICULTY_OPTIONS)
        sd.config(activebackground=constants.BACKGROUND_COLOR, bg=constants.BACKGROUND_COLOR, highlightthickness=0)
        sd["menu"].config(bg=constants.BACKGROUND_COLOR, activebackground=constants.THEME_COLOR, activeforeground=constants.BACKGROUND_COLOR)
        sd.pack(side='right')

        category_container = tkinter.Frame(self, background=constants.BACKGROUND_COLOR)
        category_container.grid(row=4, column=1, columnspan=1)

        tkinter.Label(category_container, text='Select a category:',  bg=constants.BACKGROUND_COLOR).pack(side='left')
        sc = tkinter.OptionMenu(category_container, GameState.get_instance().category, None, *category_names)
        sc.config(activebackground=constants.BACKGROUND_COLOR, bg=constants.BACKGROUND_COLOR, highlightthickness=0)
        sc["menu"].config(bg=constants.BACKGROUND_COLOR, activebackground=constants.THEME_COLOR, activeforeground=constants.BACKGROUND_COLOR)
        sc.pack(side='right')

        tkinter.Button(self, text='Start playing!', fg=constants.BACKGROUND_COLOR, background=constants.THEME_COLOR, activebackground=constants.ACTIVE_COLOR, activeforeground=constants.BACKGROUND_COLOR, command=self.on_click_play, pady=5, padx=5)\
            .grid(row=5, column=0, columnspan=2)

        # init select inputs
        GameState.get_instance().difficulty.set(constants.DIFFICULTY_OPTIONS[0])
        GameState.get_instance().category.set(category_names[0])

    def on_click_play(self):

        if not GameState.get_instance().is_valid_username():
            messagebox.showerror(title="Error", message="Please enter your username first in order to play")
            return

        if not GameState.get_instance().is_valid_difficulty():
            messagebox.showerror(title="Error", message="Please select a difficulty level first in order to play")
            return

        if not GameState.get_instance().is_valid_category():
            messagebox.showerror(title="Error", message="Please select a category first in order to play")
            return

        self.master.go_to_game_page()

    def render_table(self):

        table_view = Treeview(self)
        table_view['columns'] = ('index', 'player', 'score')

        s = tkinter.ttk.Style()
        s.theme_use("default")
        # Configure the style of Heading in Treeview widget
        s.configure('Treeview.Heading', background=constants.THEME_COLOR, foreground=constants.BACKGROUND_COLOR)
        s.map('Treeview', background=[('selected', '#79d1b8')])
        s.map('Treeview.Heading', background=[('active', constants.ACTIVE_COLOR)])

        # format our column
        table_view.column("#0", width=0, stretch=NO)
        table_view.column("index", anchor=CENTER, width=30, stretch=NO)
        table_view.column("player", anchor=SW, minwidth=50, stretch=YES)
        table_view.column("score", anchor=SE, minwidth=40, stretch=YES)

        # Create Headings
        table_view.heading("#0", text="", anchor=CENTER)
        table_view.heading("index", text="#", anchor=CENTER)
        table_view.heading("player", text="Player", anchor=CENTER)
        table_view.heading("score", text="Score", anchor=CENTER)

        # add data
        leaderboard = highscore_client.get_leaderboard()
        if leaderboard is None:
            return

        for idx, entry in enumerate(leaderboard):
            table_view.insert(parent='', index='end', iid=idx, text='',
                              values=(idx + 1, entry[0], entry[1]))

        table_view.grid(row=2, column=0, columnspan=2, sticky='snew')





