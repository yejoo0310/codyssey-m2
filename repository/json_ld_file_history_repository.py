import json

from model import QuizHistory, QuizHistoryEntry
from repository.history_repository import HistoryRepository


class JsonLdFileHistoryRepository(HistoryRepository):
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def save(self, history: QuizHistory) -> None:
        with open(self._file_path, "a", encoding="utf-8") as file:
            json.dump(self._serialize(history), file, ensure_ascii=False)
            file.write("\n")

    def _serialize(self, history: QuizHistory) -> dict:
        return {
            "@context": {
                "@vocab": "https://codyssey.dev/quiz-history#",
            },
            "@type": "QuizHistory",
            "playedAt": history.played_at(),
            "totalCount": history.total_count(),
            "correctCount": history.correct_count(),
            "score": history.score(),
            "status": history.status(),
            "entries": [self._serialize_entry(entry) for entry in history.entries()],
        }

    def _serialize_entry(self, entry: QuizHistoryEntry) -> dict:
        return {
            "@type": "QuizHistoryEntry",
            "question": entry.question(),
            "answer": entry.answer(),
            "userAnswer": entry.user_answer(),
            "answeredAt": entry.answered_at(),
            "isCorrect": entry.is_correct(),
            "hintUsed": entry.hint_used(),
        }
