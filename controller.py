from models import Quiz
import os
import json

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_record = {"score": 0, "total_count": 0, "best_count": 0}
        self.file_path = "state.json"
        self.load_state()
    
    def show_menu(self):
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
    
    def run(self):
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

    def set_default_quizzes(self):
        self.quizzes = [
            Quiz("우유가 넘어지면?", ["밀크콩", "초코우유", "아야", "커피"], 3),
            Quiz("왕이 넘어지면?", ["킹콩", "고릴라", "아야", "콩킹"], 1),
            Quiz("왕이 양쪽에 있으면?", ["여기저기", "우왕좌왕", "양쪽왕", "왕이둘"], 2),
            Quiz("Codyssey 입학연수과정에서 시험 보는 요일은?", ["월요일", "수요일", "금요일", "토요일"], 3),
            Quiz("3월은 영어로?", ["a", "b", "c", "March"], 4)
        ]
        self.save_state()
    
    def load_state(self):
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.best_record = data.get("best_record", {"score": 0, "total_count": 0, "best_count": 0})

                temp_quizzess = []
                for q in data.get("quizzes", []):
                    new_quiz = Quiz(q['question'], q['choices'], q['answer'])
                    temp_quizzess.append(new_quiz)
                if len(temp_quizzess) >= 5:
                    self.quizzes = temp_quizzess
                    print("퀴즈를 불러왔습니다.")
                else:
                    print("현재 퀴즈 문제가 5개가 되지 않습닌다. 기본 문제를 생성하겠습니다.")
                    self.set_default_quizzes()
        except FileNotFoundError:
            print("파일이 존재하지 않습니다. 기본 문제를 생성하겠습니다.")
            self.set_default_quizzes()
        except json.JSONDecodeError:
            print("state.json 파일이 손상되었습니다. 기본 문제를 생성하겠습니다.")
            self.set_default_quizzes()
        except Exception as e:
            print("오류가 발생하였습니다. 기본 문제를 생성하겠습니다.")
            self.set_default_quizzes()
    
    def save_state(self):
        try:
            data = {
                "quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "best_record": self.best_record
            }   
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            print("저장 중 오류 발생")
    
    def play_quiz(self):
        if not self.quizzes or len(self.quizzes) < 5:
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
            return
        
        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")

        current_score = 0

        for i, quiz in enumerate(self.quizzes, start = 1):
            quiz.display(i)
            user_input = self.get_valid_input()

            if user_input is None:
                return
            
            if quiz.is_correct(user_input):
                print("정답입니다!")
                current_score += 1
            else:
                print(f"틀렸습니다. 정답은 {quiz.answer}번입니다.")
        
        self.show_result(current_score)

    def show_result(self, score):
        percentage = int((score/len(self.quizzes)) * 100)
        print("\n\n========================================")
        if score == 0 or percentage == 0:
            print("한 문제도 맞히지 못했습니다.")
            return
        print(f"🏆 결과: {len(self.quizzes)}문제 중 {score}문제 정답! ({percentage}점)")
        if percentage > self.best_record["score"] or (percentage == self.best_record["score"] and len(self.quizzes) > self.best_record["total_count"]):
            print("🎉 새로운 최고 점수입니다! 최고 점수가 갱신되었습니다!")
            self.best_record = {
                "score": percentage,
                "total_count": len(self.quizzes),
                "best_count": score
            }
            self.save_state()
        print("========================================\n")

            
    def get_valid_input(self):
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
            
    def add_quiz(self):
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
            
            new_quiz = Quiz(question, choices, answer)
            self.quizzes.append(new_quiz)
            self.save_state()
            print("\n퀴즈가 정상적으로 저장되었습니다!\n")
        except (KeyboardInterrupt, EOFError):
            print("\n퀴즈 추가가 취소되었습니다. 메뉴로 돌아갑니다.\n")

    def view_quiz_list(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 추가해주세요.\n")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("\n----------------------------------------")
        for i, quiz in enumerate(self.quizzes, start = 1):
            print(f"[문제{i}] {quiz.question}")
        print("----------------------------------------")

    def show_best_score(self):
        if self.best_record["score"] == 0:
            print("\n아직 기록된 최고 점수가 없습니다.")
            return
        print(f"\n🏆 최고 점수: {self.best_record['score']}점 ({self.best_record['total_count']}문제 중 {self.best_record['best_count']}문제 정답)\n")