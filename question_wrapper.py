import utils
from question_model import QuestionModel


class QuestionWrapper:
    """
    Wraps a QuestionModel object adding useful metadata
    """

    def __init__(self, question: QuestionModel):

        self.question: QuestionModel = question
        self.timer: int = 0
        self.activation_timestamp: int = 0
        self.selected_answer: str = None

    def activate(self):

        self.activation_timestamp = utils.current_timestamp()

    def deactivate(self, answer: str):

        if self.activation_timestamp == 0:
            # skip if it was not activated yet
            return

        if utils.is_string_equals_ignore_case(self.selected_answer, answer):
            # already answered
            self.activation_timestamp = 0
            return

        # update user's answer
        self.selected_answer = answer

        delta = utils.current_timestamp() - self.activation_timestamp
        self.timer += delta
        self.activation_timestamp = 0

    def calculate_score(self) -> int:

        c = 0
        if self.is_valid():
            c = 1

        d = 1
        if utils.is_string_equals_ignore_case(self.question.difficulty, "medium"):
            d = 2
        elif utils.is_string_equals_ignore_case(self.question.difficulty, "hard"):
            d = 3

        return c * d * self.timer

    def is_valid(self) -> bool:

        return utils.is_string_equals_ignore_case(self.question.correct_answer, self.selected_answer)
