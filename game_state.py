from tkinter import StringVar, IntVar

import constants
import highscore_client
import open_tdb_client
import utils
from countdown_task import CountdownTask
from errors import QuestionGroupLimitReached
from question_wrapper import QuestionWrapper


class GameState:
    """
    Singleton class
    """
    __instance = None

    @staticmethod
    def get_instance():

        if GameState.__instance is None:
            GameState()
        return GameState.__instance

    def __init__(self):

        if GameState.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GameState.__instance = self

        self.categories: list = []
        self.username: StringVar = StringVar(value='Darthvader')
        self.difficulty: StringVar = StringVar(value='')
        self.category: StringVar = StringVar(value='')
        self.questions: list = []
        self.score: IntVar = IntVar(value=0)
        self.timer: IntVar = IntVar(value=0)
        self.index: int = -1
        self.countdown_task: CountdownTask = None
        self.user_selection: StringVar = StringVar(value='')
        self.group_count: int = 0

    def start_new_session(self):

        self.reset()
        self.next_group()

    def reset(self):

        for ti in self.timer.trace_vinfo():
            # remove any trace callbacks
            self.timer.trace_vdelete(*ti)

        self.questions = []
        self.score.set(0)
        self.timer.set(0)
        self.index = -1
        self.user_selection.set('')
        self.group_count = 0

        self.stop_countdown_task()

    def start_countdown_task(self):

        self.countdown_task = CountdownTask(self.timer)
        self.countdown_task.start()

    def stop_countdown_task(self):

        if self.countdown_task is not None:
            self.countdown_task.terminate()

    def next_group(self):

        if self.group_count >= constants.GROUP_LIMIT_PER_GAME_SESSION:
            raise QuestionGroupLimitReached

        self.timer.set(constants.TIMER_PER_GROUP)
        self.questions.clear()
        question_models = open_tdb_client.get_questions(self.get_selected_category_id(), self.difficulty.get().lower(),
                                                        constants.QUESTIONS_PER_GROUP)
        for question_model in question_models:
            # convert from question model to question wrapper
            self.questions.append(QuestionWrapper(question_model))

        self.group_count += 1

    def next_question(self) -> QuestionWrapper:

        self.index += 1
        if self.index >= constants.QUESTIONS_PER_GROUP:
            self.index = 0

        return self.get_question()

    def prev_question(self) -> QuestionWrapper:

        self.index -= 1
        if self.index < 0:
            self.index = constants.QUESTIONS_PER_GROUP - 1
        return self.get_question()

    def first_question(self) -> QuestionWrapper:

        self.index = 0
        return self.get_question()

    def last_question(self) -> QuestionWrapper:

        self.index = constants.QUESTIONS_PER_GROUP - 1
        return self.get_question()

    def get_question(self) -> QuestionWrapper:

        if self.index < 0 or self.index >= len(self.questions):
            return

        question = self.questions[self.index]
        question.activate()
        return question

    def submit_question(self):

        if self.index < 0 or self.index >= len(self.questions):
            return

        question = self.questions[self.index]
        if question is None:
            return

        question.deactivate(self.user_selection.get())

    def submit(self):

        self.stop_countdown_task()
        self.submit_question()
        self.calculate_score()

    def invalid_questions(self) -> int:

        counter: int = 0
        for question in self.questions:
            if not question.is_valid():
                counter += 1

        return counter

    def calculate_score(self):

        if self.questions is None:
            return

        for question in self.questions:
            self.score.set(self.score.get() + question.calculate_score())

    def get_categories(self):

        if not self.categories:
            self.categories = open_tdb_client.get_categories()

        return self.categories

    def get_categories_names(self) -> list:

        categories: list = self.get_categories()
        if not categories:
            return []

        category_names = []
        for category in categories:
            category_names.append(category['name'])

        return category_names

    def get_selected_category_id(self) -> int:

        selected_category: str = self.category.get()
        if utils.is_string_blank(selected_category):
            return 0

        categories: list = self.get_categories()
        if not categories:
            return 0

        for category in categories:
            if utils.is_string_equals_ignore_case(category['name'], selected_category):
                return category['id']

        return 0

    def is_valid_username(self) -> bool:

        return utils.is_string_not_blank(self.username.get())

    def is_valid_difficulty(self) -> bool:

        return utils.is_string_not_blank(self.difficulty.get())

    def is_valid_category(self) -> bool:

        return utils.is_string_not_blank(self.category.get())

    def is_highscore(self) -> bool:

        return highscore_client.is_highscore(self.score.get())

    def update_highscores(self):

        highscore_client.update_highscores(self.username.get(), self.score.get())
