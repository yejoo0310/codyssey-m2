class QuizHistoryEntry:
    def __init__(
        self,
        question: str,
        answer: int,
        user_answer: int,
        answered_at: str,
        is_correct: bool,
        hint_used: bool,
    ) -> None:
        if not isinstance(question, str):
            raise ValueError("기록 문제는 문자열이어야 합니다.")
        if not question.strip():
            raise ValueError("기록 문제는 비어있을 수 없습니다.")
        if not isinstance(answer, int):
            raise ValueError("정답 기록은 정수여야 합니다.")
        if not isinstance(user_answer, int):
            raise ValueError("사용자 답 기록은 정수여야 합니다.")
        if not isinstance(answered_at, str):
            raise ValueError("기록 시각은 문자열이어야 합니다.")
        if not answered_at.strip():
            raise ValueError("기록 시각은 비어있을 수 없습니다.")
        if not isinstance(is_correct, bool):
            raise ValueError("정오답 기록은 bool이어야 합니다.")
        if not isinstance(hint_used, bool):
            raise ValueError("힌트 사용 기록은 bool이어야 합니다.")

        self._question = question.strip()
        self._answer = answer
        self._user_answer = user_answer
        self._answered_at = answered_at.strip()
        self._is_correct = is_correct
        self._hint_used = hint_used

    def question(self) -> str:
        return self._question

    def answer(self) -> int:
        return self._answer

    def user_answer(self) -> int:
        return self._user_answer

    def answered_at(self) -> str:
        return self._answered_at

    def is_correct(self) -> bool:
        return self._is_correct

    def hint_used(self) -> bool:
        return self._hint_used
