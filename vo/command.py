class Command:
    value: int

    def __init__(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("메뉴 명령은 정수여야 합니다.")
        if value < 1 or value > 5:
            raise ValueError("범위를 넘어간 값입니다. 1-5 사이의 메뉴 번호를 입력해주세요.")

        self.value = value

    def is_play_quiz(self) -> bool:
        return self.value == 1

    def is_add_quiz(self) -> bool:
        return self.value == 2

    def is_view_quiz_list(self) -> bool:
        return self.value == 3

    def is_show_best_score(self) -> bool:
        return self.value == 4

    def is_exit(self) -> bool:
        return self.value == 5
