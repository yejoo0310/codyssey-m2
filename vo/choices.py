from vo.choice import Choice


class Choices:
    def __init__(self, choices: list[Choice]) -> None:
        if not isinstance(choices, list):
            raise ValueError("선택지는 리스트여야 합니다.")
        if len(choices) != 4:
            raise ValueError("선택지는 정확히 4개여야 합니다.")
        if not all(isinstance(choice, Choice) for choice in choices):
            raise ValueError("Choices는 Choice 객체 목록이어야 합니다.")

        self._choices = tuple(choices)

    @classmethod
    def from_texts(cls, texts: list[str]) -> "Choices":
        return cls([Choice(text) for text in texts])

    def texts(self) -> list[str]:
        return [choice.value for choice in self._choices]

    def count(self) -> int:
        return len(self._choices)
