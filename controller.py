from model import BestRecord, MultipleChoiceQuiz, Quizzes
from storage import StateStore
from vo import Answer, Choices, Question

class QuizGame:
    def __init__(self) -> None:
        self.quizzes = Quizzes()
        self.best_record = BestRecord()
        self.file_path = "state.json"
        self.state_store = StateStore(self.file_path)
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
        self.quizzes = Quizzes(
            [
                self.create_quiz("우유가 넘어지면?", ["밀크콩", "초코우유", "아야", "커피"], 3),
                self.create_quiz("왕이 넘어지면?", ["킹콩", "고릴라", "아야", "콩킹"], 1),
                self.create_quiz("왕이 양쪽에 있으면?", ["여기저기", "우왕좌왕", "양쪽왕", "왕이둘"], 2),
                self.create_quiz("Codyssey 입학연수과정에서 시험 보는 요일은?", ["월요일", "수요일", "금요일", "토요일"], 3),
                self.create_quiz("3월은 영어로?", ["a", "b", "c", "March"], 4),
            ]
        )
        self.save_state()

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
        try:
            if not self.state_store.exists():
                raise FileNotFoundError
            loaded_quizzes, loaded_record = self.state_store.load()
            if loaded_quizzes.has_minimum(5):
                self.quizzes = loaded_quizzes
                self.best_record = loaded_record
                print("퀴즈를 불러왔습니다.")
            else:
                print("현재 퀴즈 문제가 5개가 되지 않습닌다. 기본 문제를 생성하겠습니다.")
                self.set_default_quizzes()
        except FileNotFoundError:
            print("파일이 존재하지 않습니다. 기본 문제를 생성하겠습니다.")
            self.set_default_quizzes()
        except ValueError:
            print("state.json 파일이 손상되었습니다. 기본 문제를 생성하겠습니다.")
            self.set_default_quizzes()
        except Exception:
            print("state.json 파일이 손상되었습니다. 기본 문제를 생성하겠습니다.")
            self.set_default_quizzes()
    
    def save_state(self) -> None:
        try:
            self.state_store.save(self.quizzes, self.best_record)
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
        percentage = int((score / self.quizzes.count()) * 100)
        print("\n\n========================================")
        if score == 0 or percentage == 0:
            print("한 문제도 맞히지 못했습니다.")
            return
        print(f"🏆 결과: {self.quizzes.count()}문제 중 {score}문제 정답! ({percentage}점)")
        if self.best_record.should_update(percentage, self.quizzes.count()):
            print("🎉 새로운 최고 점수입니다! 최고 점수가 갱신되었습니다!")
            self.best_record.update(percentage, self.quizzes.count(), score)
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
