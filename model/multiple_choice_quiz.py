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

    def choices(self) -> list[str]:
        return self._choices.texts()

    def answer(self) -> int:
        return self._answer.value

    def answer_label(self) -> str:
        return self._answer.label()

    def display(self, index: int) -> None:
        print("\n----------------------------------------")
        print(f"[문제 {index}]")
        print(f"{self.question()}\n")
        for i, choice in enumerate(self.choices(), start=1):
            print(f"{i}. {choice}")

    def is_correct(self, user_input: int) -> bool:
        return self._answer.matches(user_input)
