from abc import ABC, abstractmethod

from model import BestRecord


class StateRepository(ABC):
    @abstractmethod
    def exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def load(self) -> BestRecord:
        raise NotImplementedError

    @abstractmethod
    def save(self, best_record: BestRecord) -> None:
        raise NotImplementedError
