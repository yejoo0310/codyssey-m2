class Choice:
    value: str

    def __init__(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("선택지는 문자열이어야 합니다.")

        normalized = value.strip()
        if not normalized:
            raise ValueError("선택지는 비어있을 수 없습니다.")

        self.value = normalized
