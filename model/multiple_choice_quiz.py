from vo.answer import Answer
from vo.choices import Choices
from vo.question import Question


class MultipleChoiceQuiz:
    def __init__(self, question: Question, choices: Choices, answer: Answer) -> None:
        self._question = question
        self._choices = choices
        self._answer = answer

    def question(self) -> str:
        return self._question.value

    def choices(self) -> Choices:
        return self._choices

    def answer(self) -> int:
        return self._answer.value

    def answer_label(self) -> str:
        return self._answer.label()

    def is_correct(self, user_answer: Answer) -> bool:
        return self._answer.matches(user_answer)
