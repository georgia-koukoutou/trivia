import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno, showinfo
from tkinter.ttk import Separator

import constants
import utils
from errors import QuestionGroupLimitReached
from game_state import GameState
from question_wrapper import QuestionWrapper


class GamePage(tkinter.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.score_label = None
        self.timer_label = None
        self.username_label = None
        self.main_container = tkinter.Frame(self)
        self.main_container.pack(fill=BOTH, expand=True)
        self.main_container.config(padx=10, pady=10, bg=constants.BACKGROUND_COLOR)
        self.center_container = None

        self.render_top()
        self.render_bottom()

        GameState.get_instance().start_new_session()
        self.next_question()
        GameState.get_instance().start_countdown_task()

        GameState.get_instance().timer.trace(mode="w", callback=self.on_timer_update)

    def render_top(self):

        top_container = tkinter.Frame(self.main_container)
        top_container.pack(fill=X, expand=False, side=TOP)
        top_container.config(height=30, bg=constants.BACKGROUND_COLOR)

        top_container.grid_columnconfigure(0, weight=1)
        top_container.grid_columnconfigure(1, weight=1)
        top_container.grid_columnconfigure(2, weight=1)

        top_container.grid_rowconfigure(0, weight=1)
        top_container.grid_rowconfigure(1, weight=1)

        self.username_label = tkinter.Label(top_container, textvariable=GameState.get_instance().username, bg=constants.BACKGROUND_COLOR)
        self.timer_label = tkinter.Label(top_container, textvariable=GameState.get_instance().timer, bg=constants.BACKGROUND_COLOR)
        self.score_label = tkinter.Label(top_container, textvariable=GameState.get_instance().score, bg=constants.BACKGROUND_COLOR)

        tkinter.Label(top_container, text='Player', bg=constants.BACKGROUND_COLOR).grid(row=0, column=0, columnspan=1, sticky='w')
        tkinter.Label(top_container, text='Timer', bg=constants.BACKGROUND_COLOR).grid(row=0, column=1, columnspan=1)
        tkinter.Label(top_container, text='Score', bg=constants.BACKGROUND_COLOR).grid(row=0, column=2, columnspan=1, sticky='e')

        self.username_label.grid(row=1, column=0, columnspan=1, sticky='w')
        self.timer_label.grid(row=1, column=1, columnspan=1)
        self.score_label.grid(row=1, column=2, columnspan=1, sticky='e')

        separator = Separator(self.main_container, orient='horizontal')
        separator.pack(fill='x', side=TOP)

    def render_bottom(self):

        bottom_container = tkinter.Frame(self.main_container, bg=constants.BACKGROUND_COLOR)
        bottom_container.pack(fill=X, expand=False, side=BOTTOM)

        btn_container = tkinter.Frame(bottom_container, bg=constants.BACKGROUND_COLOR)
        btn_container.pack()

        tkinter.Button(btn_container, text="First", command=self.first_question, pady=5, padx=5, fg=constants.BACKGROUND_COLOR, background=constants.THEME_COLOR, activebackground=constants.ACTIVE_COLOR).pack(side=LEFT, padx=5)
        tkinter.Button(btn_container, text="Previous", command=self.prev_question, pady=5, padx=5, fg=constants.BACKGROUND_COLOR, background=constants.THEME_COLOR, activebackground=constants.ACTIVE_COLOR).pack(side=LEFT, padx=5)
        tkinter.Button(btn_container, text="Next", command=self.next_question, pady=5, padx=5, fg=constants.BACKGROUND_COLOR, background=constants.THEME_COLOR, activebackground=constants.ACTIVE_COLOR).pack(side=LEFT, padx=5)
        tkinter.Button(btn_container, text="Last", command=self.last_question, pady=5, padx=5, fg=constants.BACKGROUND_COLOR, background=constants.THEME_COLOR, activebackground=constants.ACTIVE_COLOR).pack(side=LEFT, padx=5)
        tkinter.Button(btn_container, text="Submit", command=self.submit, pady=5, padx=5, fg=constants.BACKGROUND_COLOR, background=constants.THEME_COLOR, activebackground=constants.ACTIVE_COLOR).pack(side=LEFT, padx=5)

        separator = Separator(self.main_container, orient='horizontal')
        separator.pack(fill='x', side=BOTTOM, pady=5)

    def render_question(self, question_wrapper: QuestionWrapper):

        # reset
        if self.center_container is not None:
            self.center_container.destroy()
        GameState.get_instance().user_selection.set(None)

        if question_wrapper is None:
            return

        if utils.is_string_not_blank(question_wrapper.selected_answer):
            GameState.get_instance().user_selection.set(question_wrapper.selected_answer)

        self.center_container = tkinter.Frame(self.main_container)
        self.center_container.pack(fill=BOTH, expand=True, side=TOP)
        self.center_container.config(pady=10, bg=constants.BACKGROUND_COLOR)

        question_label = tkinter.Label(self.center_container, text=question_wrapper.question.text)
        # wrap text on window resize
        question_label.bind('<Configure>', lambda e: question_label.config(wraplength=self.winfo_width() - 30, bg=constants.BACKGROUND_COLOR))
        question_label.grid(row=0, column=0, sticky=W)
        for index, choice in enumerate(question_wrapper.question.choices):
            choice_label = tkinter.Radiobutton(self.center_container, text=choice, value=choice, bg=constants.BACKGROUND_COLOR, highlightthickness=0,
                                               activebackground=constants.ACTIVE_COLOR, activeforeground=constants.BACKGROUND_COLOR, 
                                               variable=GameState.get_instance().user_selection)
            choice_label.grid(row=index + 1, column=0, sticky=W, padx=10)

    def next_question(self):

        GameState.get_instance().submit_question()
        question_model = GameState.get_instance().next_question()
        self.render_question(question_model)

    def prev_question(self):

        GameState.get_instance().submit_question()
        question_model = GameState.get_instance().prev_question()
        self.render_question(question_model)

    def first_question(self):

        GameState.get_instance().submit_question()
        question_model = GameState.get_instance().first_question()
        self.render_question(question_model)

    def last_question(self):

        GameState.get_instance().submit_question()
        question_model = GameState.get_instance().last_question()
        self.render_question(question_model)

    def submit(self):

        GameState.get_instance().submit()
        is_highscore: bool = GameState.get_instance().is_highscore()
        GameState.get_instance().update_highscores()
        
        if GameState.get_instance().timer.get() <= 0:
            showinfo(message='Time is up! Thanks for playing!')
            self.master.go_to_landing_page()
            return

        if GameState.get_instance().invalid_questions() >= constants.INVALID_ANSWERS_PER_GROUP_LIMIT:
            showinfo(message='Too many invalid answers. Try again later!')
            self.master.go_to_landing_page()
            return

        confirmation = askyesno(title='Confirmation', message='Go to the next questions group?')
        if confirmation:
            try:
                GameState.get_instance().next_group()
                self.first_question()
                GameState.get_instance().start_countdown_task()
            except QuestionGroupLimitReached:
                messagebox.showerror('Game over', 'Reached maximum number of question groups. Thanks for playing!')
                self.master.go_to_landing_page()
        else:
            if is_highscore:
                score: int = GameState.get_instance().score.get()
                messagebox.showinfo("Congratulations", f'New highscore {score}!!!')

            self.master.go_to_landing_page()

    def on_timer_update(self, *args):

        if GameState.get_instance().timer.get() <= 0:
            self.submit()
