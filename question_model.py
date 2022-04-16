class QuestionModel:

    def __init__(self, text: str, correct_answer: str, choices: list, difficulty: str):
        self.text: str = text
        self.correct_answer: str = correct_answer
        self.choices: list = choices
        self.difficulty: str = difficulty
