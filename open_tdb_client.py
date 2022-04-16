import html
from random import shuffle

import requests

from question_model import QuestionModel


def get_categories() -> list:
    response = requests.get(url="https://opentdb.com/api_category.php")
    # Raises an HTTPError, if one occurred.
    response.raise_for_status()
    return response.json()['trivia_categories']


def get_questions(category_id, difficulty, amount) -> list:
    response = requests.get(
        url=f'https://opentdb.com/api.php?amount={amount}&category={category_id}&difficulty={difficulty}')
    # Raises an HTTPError, if one occurred.
    response.raise_for_status()

    results = response.json()['results']
    questions = []

    for result in results:
        choices = []
        question_text = html.unescape(result["question"])
        correct_answer = html.unescape(result["correct_answer"])
        difficulty = html.unescape(result["difficulty"])
        incorrect_answers = result["incorrect_answers"]
        for answers in incorrect_answers:
            choices.append(html.unescape(answers))
        choices.append(correct_answer)
        shuffle(choices)
        questions.append(QuestionModel(question_text, correct_answer, choices, difficulty))

    return questions
