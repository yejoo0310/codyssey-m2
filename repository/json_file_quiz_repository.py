import json
import os

from model import MultipleChoiceQuiz, Quizzes
from repository.quiz_repository import QuizRepository
from vo import Answer, Choices, Hint, Question


class JsonFileQuizRepository(QuizRepository):
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def exists(self) -> bool:
        return os.path.exists(self._file_path)

    def load(self) -> Quizzes:
        with open(self._file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("퀴즈 파일은 배열 형식이어야 합니다.")

        return Quizzes([self._deserialize(item) for item in data])

    def save(self, quizzes: Quizzes) -> None:
        data = [self._serialize(quiz) for quiz in quizzes.items()]
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _deserialize(self, data: dict) -> MultipleChoiceQuiz:
        try:
            choices = Choices.from_texts(data["choices"])
            return MultipleChoiceQuiz(
                Question(data["question"]),
                choices,
                Answer(data["answer"], choices),
                Hint(data["hint"]),
            )
        except KeyError as exc:
            raise ValueError(f"누락된 퀴즈 데이터입니다: {exc}") from exc

    def _serialize(self, quiz: MultipleChoiceQuiz) -> dict:
        return {
            "question": quiz.question(),
            "choices": quiz.choices().texts(),
            "answer": quiz.answer(),
            "hint": quiz.hint(),
        }
