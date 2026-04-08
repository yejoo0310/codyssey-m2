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
        min_value = 1
        max_value = 5
        
        print("\n========================================")
        print("         🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("========================================")

        user_input = self.get_input_number(
            prompt="선택: ",
            min_value=min_value,
            max_value=max_value,
            empty_message=f"입력이 비어있습니다. {min_value}-{max_value} 사이의 메뉴 번호를 입력해주세요.",
            invalid_message=f"잘못된 입력입니다. {min_value}-{max_value} 사이의 메뉴 번호를 입력해주세요.",
            cancel_message="\n사용자에 의해 프로그램이 강제 종료되었습니다.",
            return_none=False
        )
        
        return user_input
    
    def run(self):
        try:
            while True:
                choice = self.show_menu()

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.view_quiz_list()
                elif choice == 4:
                    self.show_best_score()
                elif choice == 5:
                    self.save_state()
                    print("퀴즈 게임이 종료되었습니다.")
                    break
        except (KeyboardInterrupt, EOFError):
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
                if len(temp_quizzess) >= 1:
                    self.quizzes = temp_quizzess
                    print("퀴즈를 불러왔습니다.")
                else:
                    print("현재 문제가 하나도 없습니다. 기본 문제를 생성하겠습니다.")
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

    def get_input_number(self, prompt, min_value, max_value, empty_message, invalid_message, cancel_message, return_none):
        while True:
            try:
                value = input(prompt).strip()
                
                if not value:
                    print(empty_message)
                    continue
                
                number = int(value)
                
                if min_value <= number <= max_value:
                    return number
                
                print(invalid_message)
            except ValueError:
                print(invalid_message)
            except (KeyboardInterrupt, EOFError):
                print(cancel_message)
                if return_none:
                    return None
                raise 
    
    def get_input_string(self, prompt, empty_message, cancel_message, return_none):
        while True:
            try:
                value = input(prompt).strip()

                if not value:
                    print(empty_message)
                    continue
                
                return value
            except (KeyboardInterrupt, EOFError):
                print(cancel_message)
                if return_none:
                    return None
                raise
    
    def play_quiz(self):
        min_value = 1
        max_value = 4
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
            return
        
        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")

        current_score = 0

        for i, quiz in enumerate(self.quizzes, start = 1):
            quiz.display(i)
            user_input = self.get_input_number(
                prompt="\n정답 입력: ",
                min_value=min_value,
                max_value=max_value,
                empty_message=f"입력이 비어있습니다. {min_value}-{max_value} 사이의 번호를 입력해주세요.",
                invalid_message=f"잘못된 입력입니다. {min_value}-{max_value} 사이의 번호를 입력해주세요.",
                cancel_message="\n사용자에 의해 퀴즈 풀기를 중단합니다.",
                return_none=True
            )

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

            
    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        
        question = self.get_input_string(
            prompt="문제를 입력하세요: ",
            empty_message="문제는 비어있을 수 없습니다. 다시 입력해주세요.",
            cancel_message="\n퀴즈 추가가 취소되었습니다. 메뉴로 돌아갑니다.\n",
            return_none=True
        )
        if question is None:
            return
        
        choices = []
        for i in range(1, 5):
            choice = self.get_input_string(
                prompt=f"선택지 {i}: ",
                empty_message=f"선택지 {i}은(는) 비어있을 수 없습니다. 다시 입력해주세요.",
                cancel_message="\n퀴즈 추가가 취소되었습니다. 메뉴로 돌아갑니다.\n",
                return_none=True
            )
            if choice is None:
                return
            choices.append(choice)
        
        min_value=1
        max_value=4
        answer = self.get_input_number(
            prompt=f"정답 번호 ({min_value}-{max_value}): ",
            min_value=min_value,
            max_value=max_value,
            empty_message="정답은 비어있을 수 없습니다. 다시 입력해주세요.",
            invalid_message=f"잘못된 입력입니다. {min_value}-{max_value} 사이의 정답 번호를 입력해주세요.",
            cancel_message="\n퀴즈 추가가 취소되었습니다. 메뉴로 돌아갑니다.\n",
            return_none=True
        )
        if answer is None:
            return
        
        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n퀴즈가 정상적으로 저장되었습니다!\n")
        

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