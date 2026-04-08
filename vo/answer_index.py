class AnswerIndex:
    def __init__(self, value):
        if not isinstance(value, int):
            raise ValueError("정답 번호는 정수여야 합니다.")
        if value < 1 or value > 4:
            raise ValueError("정답 번호는 1-4 사이여야 합니다.")
        self._value = value

    @property
    def value(self):
        return self._value

    def matches(self, user_input):
        return self._value == user_input
