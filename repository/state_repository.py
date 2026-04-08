import json
import os

from model import BestRecord


class StateRepository:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def exists(self) -> bool:
        return os.path.exists(self._file_path)

    def load(self) -> BestRecord:
        with open(self._file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return self._deserialize_best_record(data)

    def save(self, best_record: BestRecord) -> None:
        data = self._serialize_best_record(best_record)
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _deserialize_best_record(self, data: dict) -> BestRecord:
        if not isinstance(data, dict):
            raise ValueError("state.json 파일은 객체 형식이어야 합니다.")

        try:
            return BestRecord(
                data["score"],
                data["total_count"],
                data["best_count"],
            )
        except KeyError as exc:
            raise ValueError(f"누락된 상태 데이터입니다: {exc}") from exc

    def _serialize_best_record(self, best_record: BestRecord) -> dict:
        return {
            "score": best_record.score(),
            "total_count": best_record.total_count(),
            "best_count": best_record.best_count(),
        }
