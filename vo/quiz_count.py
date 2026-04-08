class QuizCount:
    value: int

    def __init__(self, value: int, max_count: int) -> None:
        if not isinstance(value, int):
            raise ValueError("문제 개수는 정수여야 합니다.")
        if not isinstance(max_count, int):
            raise ValueError("최대 문제 개수는 정수여야 합니다.")
        if max_count < 1:
            raise ValueError("최대 문제 개수는 1 이상이어야 합니다.")
        if value < 1:
            raise ValueError("문제 개수는 1 이상이어야 합니다.")
        if value > max_count:
            raise ValueError(
                f"범위를 넘어간 값입니다. 1-{max_count} 사이의 문제 개수를 입력해주세요."
            )

        self.value = value
