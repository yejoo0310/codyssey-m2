from vo.choices import Choices


class Answer:
    value: int

    def __init__(self, value: int, choices: Choices) -> None:
        if not isinstance(value, int):
            raise ValueError("정답 번호는 정수여야 합니다.")
        if value < 1 or value > choices.count():
            raise ValueError(
                f"범위를 넘어간 값입니다. 1-{choices.count()} 사이의 번호를 입력해주세요."
            )

        self.value = value

    def label(self) -> str:
        return f"{self.value}번"

    def matches(self, answer: "Answer") -> bool:
        return self.value == answer.value
