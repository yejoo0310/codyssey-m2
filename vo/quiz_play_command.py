class QuizPlayCommand:
    value: str

    def __init__(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("퀴즈 명령은 문자열이어야 합니다.")
        if value != "/hint":
            raise ValueError("지원하지 않는 퀴즈 명령입니다.")

        self.value = value

    def is_show_hint(self) -> bool:
        return self.value == "/hint"
