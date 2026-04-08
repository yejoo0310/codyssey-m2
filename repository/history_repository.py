from abc import ABC, abstractmethod

from model import QuizHistory


class HistoryRepository(ABC):
    @abstractmethod
    def save(self, history: QuizHistory) -> None:
        raise NotImplementedError
