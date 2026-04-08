from model.quiz_history_entry import QuizHistoryEntry


class QuizHistory:
    def __init__(
        self,
        played_at: str,
        total_count: int,
        correct_count: int,
        entries: list[QuizHistoryEntry],
        status: str,
    ) -> None:
        if not isinstance(played_at, str):
            raise ValueError("세션 시각은 문자열이어야 합니다.")
        if not played_at.strip():
            raise ValueError("세션 시각은 비어있을 수 없습니다.")
        if not isinstance(total_count, int):
            raise ValueError("총 문제 수는 정수여야 합니다.")
        if not isinstance(correct_count, int):
            raise ValueError("정답 수는 정수여야 합니다.")
        if total_count < 1:
            raise ValueError("총 문제 수는 1 이상이어야 합니다.")
        if correct_count < 0:
            raise ValueError("정답 수는 0 이상이어야 합니다.")
        if correct_count > total_count:
            raise ValueError("정답 수는 총 문제 수를 초과할 수 없습니다.")
        if not isinstance(entries, list):
            raise ValueError("기록 목록은 리스트여야 합니다.")
        if not all(isinstance(entry, QuizHistoryEntry) for entry in entries):
            raise ValueError("기록 목록은 QuizHistoryEntry 목록이어야 합니다.")
        if not isinstance(status, str):
            raise ValueError("기록 상태는 문자열이어야 합니다.")
        if status not in ("completed", "aborted"):
            raise ValueError("기록 상태는 completed 또는 aborted여야 합니다.")

        self._played_at = played_at.strip()
        self._total_count = total_count
        self._correct_count = correct_count
        self._entries = list(entries)
        self._status = status

    def played_at(self) -> str:
        return self._played_at

    def total_count(self) -> int:
        return self._total_count

    def correct_count(self) -> int:
        return self._correct_count

    def score(self) -> int:
        return int((self._correct_count / self._total_count) * 100)

    def entries(self) -> list[QuizHistoryEntry]:
        return list(self._entries)

    def status(self) -> str:
        return self._status
