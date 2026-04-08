from vo.choices import Choices


class Answer:
    value: int

    def __init__(self, value: int, choices: Choices) -> None:
        if not isinstance(value, int):
            raise ValueError("정답 번호는 정수여야 합니다.")
        if value < 1 or value > choices.count():
            raise ValueError(f"정답 번호는 1-{choices.count()} 사이여야 합니다.")

        self.value = value

    def label(self) -> str:
        return f"{self.value}번"

    def matches(self, user_input: int) -> bool:
        return self.value == user_input
