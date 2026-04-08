import json
import os

from model import BestRecord, MultipleChoiceQuiz
from vo import AnswerIndex, ChoiceList, QuestionText


class StateStore:
    def __init__(self, file_path):
        self._file_path = file_path

    def exists(self):
        return os.path.exists(self._file_path)

    def load(self):
        with open(self._file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        quizzes = [self._deserialize_quiz(item) for item in data.get("quizzes", [])]
        best_record = self._deserialize_best_record(data.get("best_record", {}))
        return quizzes, best_record

    def save(self, quizzes, best_record):
        data = {
            "quizzes": [self._serialize_quiz(quiz) for quiz in quizzes],
            "best_record": self._serialize_best_record(best_record),
        }
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _deserialize_quiz(self, data):
        try:
            return MultipleChoiceQuiz(
                QuestionText(data["question"]),
                ChoiceList(data["choices"]),
                AnswerIndex(data["answer"]),
            )
        except KeyError as exc:
            raise ValueError(f"누락된 퀴즈 데이터입니다: {exc}") from exc

    def _serialize_quiz(self, quiz):
        return {
            "question": quiz.question_text(),
            "choices": quiz.choice_texts(),
            "answer": quiz.answer_number(),
        }

    def _deserialize_best_record(self, data):
        if not isinstance(data, dict):
            return BestRecord()
        return BestRecord(
            data.get("score", 0),
            data.get("total_count", 0),
            data.get("best_count", 0),
        )

    def _serialize_best_record(self, best_record):
        return {
            "score": best_record.score(),
            "total_count": best_record.total_count(),
            "best_count": best_record.best_count(),
        }
