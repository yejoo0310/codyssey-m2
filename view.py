from model import BestRecord, MultipleChoiceQuiz, Quizzes
from vo import Answer, Command


class ConsoleView:
    def show_menu(self) -> Command | None:
        print("\n========================================")
        print("         🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("========================================")

        user_input = input("선택: ").strip()
        if not user_input:
            self.show_menu_input_empty()
            return None

        try:
            command_value = int(user_input)
        except ValueError:
            self.show_menu_input_invalid()
            return None

        try:
            return Command(command_value)
        except ValueError as error:
            self.show_error_message(str(error))
            return None

    def show_menu_input_empty(self) -> None:
        print("입력이 비어있습니다. 1-5 사이의 메뉴 번호를 입력해주세요.")

    def show_menu_input_invalid(self) -> None:
        print("잘못된 입력입니다. 1-5 사이의 메뉴 번호를 입력해주세요.")

    def show_program_interrupted(self) -> None:
        print("\n사용자에 의해 프로그램이 강제 종료되었습니다.")

    def show_state_reset(self) -> None:
        print("state.json 파일이 손상되었습니다. 최고 기록을 초기화합니다.")

    def show_quiz_file_missing(self) -> None:
        print("quiz.json 파일이 존재하지 않습니다. 기본 문제를 생성하겠습니다.")

    def show_quiz_file_corrupted(self) -> None:
        print("quiz.json 파일이 손상되었습니다. 기본 문제를 생성하겠습니다.")

    def show_not_enough_quizzes(self) -> None:
        print("현재 퀴즈 문제가 5개가 되지 않습닌다. 기본 문제를 생성하겠습니다.")

    def show_quizzes_loaded(self) -> None:
        print("퀴즈를 불러왔습니다.")

    def show_save_error(self) -> None:
        print("저장 중 오류 발생")

    def show_error_message(self, message: str) -> None:
        print(message)

    def show_no_quizzes_for_play(self) -> None:
        print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")

    def show_quiz_start(self, total_count: int) -> None:
        print(f"\n📝 퀴즈를 시작합니다! (총 {total_count}문제)")

    def show_quiz(self, quiz: MultipleChoiceQuiz, index: int) -> None:
        print("\n----------------------------------------")
        print(f"[문제 {index}]")
        print(f"{quiz.question()}\n")
        for number, choice in enumerate(quiz.choices().texts(), start=1):
            print(f"{number}. {choice}")

    def get_answer_input(self, quiz: MultipleChoiceQuiz) -> Answer | None:
        while True:
            try:
                user_input = input("\n정답 입력: ").strip()
                if not user_input:
                    print("입력이 비어있습니다. 1-4 사이의 번호를 입력해주세요.")
                    continue

                try:
                    answer_value = int(user_input)
                except ValueError:
                    print("잘못된 입력입니다. 1-4 사이의 번호를 입력해주세요.")
                    continue

                return Answer(answer_value, quiz.choices())
            except ValueError as error:
                print(str(error))
            except (KeyboardInterrupt, EOFError):
                print("\n사용자에 의해 퀴즈 풀기를 중단합니다.\n")
                return None

    def show_correct_answer(self) -> None:
        print("정답입니다!")

    def show_incorrect_answer(self, answer_label: str) -> None:
        print(f"틀렸습니다. 정답은 {answer_label}입니다.")

    def show_result(self, total_count: int, count: int, is_new_best: bool) -> None:
        percentage = int((count / total_count) * 100)
        print("\n\n========================================")
        if count == 0 or percentage == 0:
            print("한 문제도 맞히지 못했습니다.")
            return

        print(f"🏆 결과: {total_count}문제 중 {count}문제 정답! ({percentage}점)")
        if is_new_best:
            print("🎉 새로운 최고 점수입니다! 최고 점수가 갱신되었습니다!")
        print("========================================\n")

    def get_new_quiz_form(self) -> tuple[str, list[str], int] | None:
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        try:
            return (
                self._get_question_input(),
                self._get_choices_input(),
                self._get_new_quiz_answer_input(),
            )
        except (KeyboardInterrupt, EOFError):
            print("\n퀴즈 추가가 취소되었습니다. 메뉴로 돌아갑니다.\n")
            return None

    def _get_question_input(self) -> str:
        return input("문제를 입력하세요: ")

    def _get_choices_input(self) -> list[str]:
        return [input(f"선택지 {index}: ") for index in range(1, 5)]

    def _get_new_quiz_answer_input(self) -> int:
        while True:
            answer = input("정답 번호 (1-4): ").strip()
            if not answer:
                print("정답은 비어있을 수 없습니다. 다시 입력해주세요.")
                continue

            try:
                answer_number = int(answer)
            except ValueError:
                print("잘못된 입력입니다. 1-4 사이의 정답 번호를 입력해주세요.")
                continue

            return answer_number

    def show_quiz_saved(self) -> None:
        print("\n퀴즈가 정상적으로 저장되었습니다!\n")

    def show_quiz_list(self, quizzes: Quizzes) -> None:
        if quizzes.is_empty():
            print("\n등록된 퀴즈가 없습니다. 먼저 추가해주세요.\n")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {quizzes.count()}개)")
        print("\n----------------------------------------")
        for index, quiz in enumerate(quizzes.items(), start=1):
            print(f"[문제{index}] {quiz.question()}")
        print("----------------------------------------")

    def show_best_record(self, best_record: BestRecord) -> None:
        if not best_record.has_score():
            print("\n아직 기록된 최고 점수가 없습니다.")
            return
        print(f"\n🏆 최고 점수: {best_record.summary_text()}\n")
