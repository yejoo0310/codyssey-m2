from abc import ABC, abstractmethod

from model import Quizzes


class QuizRepository(ABC):
    @abstractmethod
    def exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def load(self) -> Quizzes:
        raise NotImplementedError

    @abstractmethod
    def save(self, quizzes: Quizzes) -> None:
        raise NotImplementedError
