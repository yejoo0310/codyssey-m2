from models import Quiz
import os
import json

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.file_path = "state.json"
        self.load_state()
    
    def show_menu(self):
        print("========================================")
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
                    print("퀴즈 풀기")
                    # self.play_quiz()
                elif cmd == 2:
                    print("퀴즈 추가")
                    # self.add_quiz()
                elif cmd == 3:
                    print("퀴즈 목록")
                    # self.view_quiz_list()
                elif cmd == 4:
                    print("점수 확인")
                    # self.show_best_score()
                elif cmd == 5:
                    print("프로그램 종료")
                    self.save_state()
                    break
        except (KeyboardInterrupt, EOFError):
            print("사용자에 의해 프로그램이 강제 종료되었습니다.")
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
                self.best_score = data.get("best_score", 0)

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
                "best_score": self.best_score
            }   
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            print("저장 중 오류 발생")