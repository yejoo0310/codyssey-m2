import json
import os

from model import BestRecord, MultipleChoiceQuiz, Quizzes
from vo import Answer, Choices, Question


class StateStore:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def exists(self) -> bool:
        return os.path.exists(self._file_path)

    def load(self) -> tuple[Quizzes, BestRecord]:
        with open(self._file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        quizzes = Quizzes(
            [self._deserialize_quiz(item) for item in data.get("quizzes", [])]
        )
        best_record = self._deserialize_best_record(data.get("best_record", {}))
        return quizzes, best_record

    def save(self, quizzes: Quizzes, best_record: BestRecord) -> None:
        data = {
            "quizzes": [self._serialize_quiz(quiz) for quiz in quizzes.items()],
            "best_record": self._serialize_best_record(best_record),
        }
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _deserialize_quiz(self, data: dict) -> MultipleChoiceQuiz:
        try:
            choices = Choices.from_texts(data["choices"])
            return MultipleChoiceQuiz(
                Question(data["question"]),
                choices,
                Answer(data["answer"], choices),
            )
        except KeyError as exc:
            raise ValueError(f"누락된 퀴즈 데이터입니다: {exc}") from exc

    def _serialize_quiz(self, quiz: MultipleChoiceQuiz) -> dict:
        return {
            "question": quiz.question(),
            "choices": quiz.choices(),
            "answer": quiz.answer(),
        }

    def _deserialize_best_record(self, data: dict) -> BestRecord:
        if not isinstance(data, dict):
            return BestRecord()
        return BestRecord(
            data.get("score", 0),
            data.get("total_count", 0),
            data.get("best_count", 0),
        )

    def _serialize_best_record(self, best_record: BestRecord) -> dict:
        return {
            "score": best_record.score(),
            "total_count": best_record.total_count(),
            "best_count": best_record.best_count(),
        }
