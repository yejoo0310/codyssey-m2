class BestRecord:
    def __init__(
        self, score: int = 0, total_count: int = 0, best_count: int = 0
    ) -> None:
        self._score = self._require_non_negative(score, "score")
        self._total_count = self._require_non_negative(total_count, "total_count")
        self._best_count = self._require_non_negative(best_count, "best_count")

    def _require_non_negative(self, value: int, field_name: str) -> int:
        if not isinstance(value, int):
            raise ValueError(f"{field_name}는 정수여야 합니다.")
        if value < 0:
            raise ValueError(f"{field_name}는 0 이상이어야 합니다.")
        return value

    def _calculate_score(self, total_count: int, best_count: int) -> int:
        total_count = self._require_non_negative(total_count, "total_count")
        best_count = self._require_non_negative(best_count, "best_count")

        if total_count == 0:
            raise ValueError("total_count는 0보다 커야 합니다.")
        if best_count > total_count:
            raise ValueError("best_count는 total_count보다 클 수 없습니다.")

        return int((best_count / total_count) * 100)

    def update(self, total_count: int, best_count: int) -> bool:
        score = self._calculate_score(total_count, best_count)

        should_update = score > self._score or (
            score == self._score and total_count > self._total_count
        )
        if not should_update:
            return False

        self._score = score
        self._total_count = total_count
        self._best_count = best_count
        return True

    def has_score(self) -> bool:
        return self._score > 0

    def score(self) -> int:
        return self._score

    def total_count(self) -> int:
        return self._total_count

    def best_count(self) -> int:
        return self._best_count

    def summary_text(self) -> str:
        return (
            f"{self._score}점 "
            f"({self._total_count}문제 중 {self._best_count}문제 정답)"
        )
