import random

from model.multiple_choice_quiz import MultipleChoiceQuiz


class Quizzes:
    def __init__(self, value: list[MultipleChoiceQuiz] | None = None) -> None:
        quizzes = [] if value is None else value
        if not isinstance(quizzes, list):
            raise ValueError("퀴즈 목록은 리스트여야 합니다.")
        if not all(isinstance(quiz, MultipleChoiceQuiz) for quiz in quizzes):
            raise ValueError("Quizzes는 MultipleChoiceQuiz 목록이어야 합니다.")

        self.value = quizzes

    def add(self, quiz: MultipleChoiceQuiz) -> None:
        if not isinstance(quiz, MultipleChoiceQuiz):
            raise ValueError("추가할 대상은 MultipleChoiceQuiz여야 합니다.")
        self.value.append(quiz)

    def count(self) -> int:
        return len(self.value)

    def is_empty(self) -> bool:
        return self.count() == 0

    def has_minimum(self, count: int) -> bool:
        return self.count() >= count

    def items(self) -> list[MultipleChoiceQuiz]:
        return list(self.value)

    def pick_random(self, count: int) -> list[MultipleChoiceQuiz]:
        if not isinstance(count, int):
            raise ValueError("선택할 문제 수는 정수여야 합니다.")
        if count < 1:
            raise ValueError("선택할 문제 수는 1 이상이어야 합니다.")
        if count > self.count():
            raise ValueError("선택할 문제 수는 보유한 퀴즈 수를 초과할 수 없습니다.")

        return random.sample(self.value, count)
