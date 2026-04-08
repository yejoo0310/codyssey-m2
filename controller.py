from model import BestRecord, MultipleChoiceQuiz, Quizzes
from repository import QuizRepository, StateRepository
from vo import Answer, Choices, Question


class QuizGame:
    def __init__(self) -> None:
        self.quizzes = Quizzes()
        self.best_record = BestRecord()
        self.state_repository = StateRepository("state.json")
        self.quiz_repository = QuizRepository("quiz.json")
        self.default_quiz_repository = QuizRepository("default-quiz.json")
        self.load_state()
    
    def show_menu(self) -> int | None:
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
            print("입력이 비어있습니다. 1-5 사이의 메뉴 번호를 입력해주세요.")
            return None
        
        try:
            cmd = int(user_input)

            if 1 <= cmd <= 5:
                return cmd
            print("범위를 넘어간 값입니다. 1-5 사이의 메뉴 번호를 입력해주세요.")
            return None
        except ValueError:
            print("잘못된 입력입니다. 1-5 사이의 메뉴 번호를 입력해주세요.")
            return None
    
    def run(self) -> None:
        try:
            while True:
                cmd = self.show_menu()
                if cmd is None:
                    continue

                if cmd == 1:
                    self.play_quiz()
                elif cmd == 2:
                    self.add_quiz()
                elif cmd == 3:
                    self.view_quiz_list()
                elif cmd == 4:
                    self.show_best_score()
                elif cmd == 5:
                    self.save_state()
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n사용자에 의해 프로그램이 강제 종료되었습니다.")
            self.save_state()

    def set_default_quizzes(self) -> None:
        self.quizzes = self.default_quiz_repository.load()
        self.quiz_repository.save(self.quizzes)

    def restore_default_quizzes(self) -> None:
        try:
            self.set_default_quizzes()
        except FileNotFoundError:
            raise RuntimeError("default-quiz.json 파일이 존재하지 않습니다.")
        except ValueError as exc:
            raise RuntimeError("default-quiz.json 파일이 손상되었습니다.") from exc

    def create_quiz(
        self, question: str, choices: list[str], answer: int
    ) -> MultipleChoiceQuiz:
        choices_vo = Choices.from_texts(choices)
        return MultipleChoiceQuiz(
            Question(question),
            choices_vo,
            Answer(answer, choices_vo),
        )
    
    def load_state(self) -> None:
        self.load_best_record()
        self.load_quizzes()

    def load_best_record(self) -> None:
        try:
            if not self.state_repository.exists():
                self.best_record = BestRecord()
                return
            self.best_record = self.state_repository.load()
        except FileNotFoundError:
            self.best_record = BestRecord()
        except ValueError:
            print("state.json 파일이 손상되었습니다. 최고 기록을 초기화합니다.")
            self.best_record = BestRecord()
        except Exception:
            print("state.json 파일이 손상되었습니다. 최고 기록을 초기화합니다.")
            self.best_record = BestRecord()

    def load_quizzes(self) -> None:
        try:
            if not self.quiz_repository.exists():
                print("quiz.json 파일이 존재하지 않습니다. 기본 문제를 생성하겠습니다.")
                self.restore_default_quizzes()
                return

            loaded_quizzes = self.quiz_repository.load()
            if loaded_quizzes.has_minimum(5):
                self.quizzes = loaded_quizzes
                print("퀴즈를 불러왔습니다.")
                return

            print("현재 퀴즈 문제가 5개가 되지 않습닌다. 기본 문제를 생성하겠습니다.")
            self.restore_default_quizzes()
        except FileNotFoundError:
            print("quiz.json 파일이 존재하지 않습니다. 기본 문제를 생성하겠습니다.")
            self.restore_default_quizzes()
        except ValueError:
            print("quiz.json 파일이 손상되었습니다. 기본 문제를 생성하겠습니다.")
            self.restore_default_quizzes()
    
    def save_state(self) -> None:
        try:
            self.state_repository.save(self.best_record)
            self.quiz_repository.save(self.quizzes)
        except Exception:
            print("저장 중 오류 발생")
    
    def play_quiz(self) -> None:
        if self.quizzes.is_empty() or not self.quizzes.has_minimum(5):
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
            return
        
        print(f"\n📝 퀴즈를 시작합니다! (총 {self.quizzes.count()}문제)")

        current_score = 0

        for i, quiz in enumerate(self.quizzes.items(), start = 1):
            quiz.display(i)
            user_input = self.get_valid_input()

            if user_input is None:
                return
            
            if quiz.is_correct(user_input):
                print("정답입니다!")
                current_score += 1
            else:
                print(f"틀렸습니다. 정답은 {quiz.answer_label()}입니다.")
        
        self.show_result(current_score)

    def show_result(self, score: int) -> None:
        total_count = self.quizzes.count()
        percentage = int((score / total_count) * 100)
        print("\n\n========================================")
        if score == 0 or percentage == 0:
            print("한 문제도 맞히지 못했습니다.")
            return
        print(f"🏆 결과: {total_count}문제 중 {score}문제 정답! ({percentage}점)")
        if self.best_record.update(total_count, score):
            print("🎉 새로운 최고 점수입니다! 최고 점수가 갱신되었습니다!")
            self.save_state()
        print("========================================\n")

            
    def get_valid_input(self) -> int | None:
        while True:
            try:
                user_input = input("\n정답 입력: ")
                if not user_input:
                    print("입력이 비어있습니다. 1-4 사이의 번호를 입력해주세요.")
                    continue

                ans = int(user_input)
                if 1 <= ans <= 4: 
                    return ans
                print("범위를 넘어간 값입니다. 1-4 사이의 번호를 입력해주세요.")
            except ValueError:
                print("잘못된 입력입니다. 1-4 사이의 번호를 입력해주세요.")
            except (KeyboardInterrupt, EOFError):
                print("\n사용자에 의해 퀴즈 풀기를 중단합니다.\n")
                return None
            
    def add_quiz(self) -> None:
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        try:
            while True:
                question = input("문제를 입력하세요: ").strip()
                if question:
                    break
                print("문제는 비어있을 수 없습니다. 다시 입력해주세요.")
            
            choices = []
            for i in range(1, 5):
                while True:
                    choice = input(f"선택지 {i}: ").strip()
                    if choice:
                        choices.append(choice)
                        break
                    print(f"선택지 {i}은(는) 비어있을 수 없습니다. 다시 입력해주세요.") 
            
            while True:
                answer = input("정답 번호 (1-4): ").strip()
                if not answer:
                    print("정답은 비어있을 수 없습니다. 다시 입력해주세요.")
                    continue

                try:
                    answer = int(answer)
                    if 1 <= answer <= 4:
                        break
                    print("범위를 넘어갔습니다. 1-4 사이의 정답 번호를 입력해주세요.")
                except ValueError:
                    print("잘못된 입력입니다. 1-4 사이의 정답 번호를 입력해주세요.")
            
            new_quiz = self.create_quiz(question, choices, answer)
            self.quizzes.add(new_quiz)
            self.save_state()
            print("\n퀴즈가 정상적으로 저장되었습니다!\n")
        except (KeyboardInterrupt, EOFError):
            print("\n퀴즈 추가가 취소되었습니다. 메뉴로 돌아갑니다.\n")

    def view_quiz_list(self) -> None:
        if self.quizzes.is_empty():
            print("\n등록된 퀴즈가 없습니다. 먼저 추가해주세요.\n")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {self.quizzes.count()}개)")
        print("\n----------------------------------------")
        for i, quiz in enumerate(self.quizzes.items(), start = 1):
            print(f"[문제{i}] {quiz.question()}")
        print("----------------------------------------")

    def show_best_score(self) -> None:
        if not self.best_record.has_score():
            print("\n아직 기록된 최고 점수가 없습니다.")
            return
        print(f"\n🏆 최고 점수: {self.best_record.summary_text()}\n")
