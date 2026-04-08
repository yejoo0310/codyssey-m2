from abc import ABC, abstractmethod


class Quiz(ABC):
    def __init__(self, question_text, choice_list, answer_index):
        self._question_text = question_text
        self._choice_list = choice_list
        self._answer_index = answer_index

    def question_text(self):
        return self._question_text.value

    def choice_texts(self):
        return self._choice_list.values

    def answer_number(self):
        return self._answer_index.value

    def answer_label(self):
        return f"{self.answer_number()}번"

    @abstractmethod
    def display(self, index):
        raise NotImplementedError

    @abstractmethod
    def is_correct(self, user_input):
        raise NotImplementedError
