class QuestionText:
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("문제는 문자열이어야 합니다.")

        normalized = value.strip()
        if not normalized:
            raise ValueError("문제는 비어있을 수 없습니다.")

        self._value = normalized

    @property
    def value(self):
        return self._value
