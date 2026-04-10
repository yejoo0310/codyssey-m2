from quiz import Quiz
import os
import json
import random
from datetime import datetime

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_record = {"score": 0, "total_count": 0, "best_count": 0}
        self.history = []
        self.file_path = "state.json"
        self.load_state()
    
    def show_menu(self):
        min_value = 1
        max_value = 6
        
        print("\n========================================")
        print("         🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
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
                    self.delete_quiz()
                elif choice == 6:
                    self.save_state()
                    print("퀴즈 게임이 종료되었습니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            self.save_state()

    def set_default_quizzes(self):
        self.quizzes = [
            Quiz("우유가 넘어지면?", ["밀크콩", "초코우유", "아야", "커피"], 3, "고개를 돌려서 '우유'를 보세요."),
            Quiz("왕이 넘어지면?", ["킹콩", "고릴라", "아야", "콩킹"], 1, "왕의 영어 표현을 생각해보세요."),
            Quiz("왕이 양쪽에 있으면?", ["여기저기", "우왕좌왕", "양쪽왕", "왕이둘"], 2, "왕이 왼쪽에도 있고 오른쪽에도 있는 상황을 떠올려보세요."),
            Quiz("바나나가 웃으면?", ["바나나우유", "바나나", "바나나킥", "킥킥"], 3, "바나나 맛이 나는 과자 이름입니다."),
            Quiz("모두 일어나게 하는 숫자는?", ["하나", "둘", "셋", "다섯"], 4, "초성힌트: 'ㄷㅅ'")
        ]
        self.save_state()
    
    def load_state(self):
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.best_record = data.get("best_record", {"score": 0, "total_count": 0, "best_count": 0})
                self.history = data.get("history", [])
                
                temp_quizzess = []
                for q in data.get("quizzes", []):
                    new_quiz = Quiz(q['question'], q['choices'], q['answer'], q['hint'])
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
        except PermissionError:
            print("파일의 권한이 없어 접근에 실패하였습니다. 기본 문제를 생성하겠습니다.")
            self.set_default_quizzes()
        except Exception as e:
            print("오류가 발생하였습니다. 기본 문제를 생성하겠습니다.")
            self.set_default_quizzes()
    
    def save_state(self):
        try:
            data = {
                "quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "best_record": self.best_record,
                "history": self.history
            }   
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            print("저장 중 오류 발생")
            
    def add_history(self, started_at, score, total_count, correct_count):
        record = {
            "played_at": started_at.strftime("%Y-%m-%d %H:%M:%S"),
            "score": score,
            "total_count": total_count,
            "correct_count": correct_count
        }
        self.history.append(record)

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
    
    def get_question_count(self):
        total_count = len(self.quizzes)
        
        return self.get_input_number(
            prompt=f"\n출제할 문제 수를 입력하세요 (총 {total_count}개): ",
            min_value=1,
            max_value=total_count,
            empty_message=f"입력이 비어있습니다. 1-{total_count} 사이의 숫자를 입력해주세요.",
            invalid_message=f"잘못된 입력입니다. 1-{total_count} 사이의 숫자를 입력해주세요.",
            cancel_message="\n사용자에 의해 문제 수 선택이 취소되었습니다.\n",
            return_none=True
        )
    
    def get_random_quizzes(self, question_count):
        return random.sample(self.quizzes, question_count)
    
    def get_need_hint(self, prompt, empty_message, invalid_message, cancel_message):
        while True:
            try:
                value = input(prompt).strip().lower()
                
                if not value:
                    print(empty_message)
                    continue
                
                if value in ("y", "n"):
                    return value
                
                print(invalid_message)
            except (KeyboardInterrupt, EOFError):
                print(cancel_message)
                return None
    
    def play_quiz(self):
        min_value = 1
        max_value = 4
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
            return
        
        question_count = self.get_question_count()
        if question_count is None:
            return
        
        selected_quizzes = self.get_random_quizzes(question_count)
        
        print(f"\n📝 퀴즈를 시작합니다! (총 {question_count}문제)")
        started_at = datetime.now()

        current_score = 0
        current_count = 0

        for i, quiz in enumerate(selected_quizzes, start = 1):
            quiz.display(i)
            
            hint_used = False
            hint_choice = self.get_need_hint(
                prompt="힌트를 보시겠습니까? (y/n): ",
                empty_message="입력이 비어있습니다. 'y' 또는 'n'을 입력해주세요.",
                invalid_message="잘못된 입력입니다. 'y' 또는 'n'을 입력해주세요.",
                cancel_message="\n사용자에 의해 퀴즈 풀기를 중단합니다.\n"
            )
            if hint_choice is None:
                return
            
            if hint_choice == 'y':
                print(f"[힌트] {quiz.hint}")
                hint_used = True
            
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
            
            earned_score = quiz.calculate_score(user_input, hint_used)
            current_score += earned_score
            
            if quiz.is_correct(user_input):
                current_count += 1
                if hint_used:
                    print("\n정답입니다! (힌트 사용: 1점)")
                else:
                    print("\n정답입니다! (힌트 미사용: 2점)")
            else:
                print("\n틀렸습니다. (0점)")
                print(f"정답은 {quiz.answer}번입니다.")
        
        self.show_result(current_score, current_count, question_count, started_at)

    def show_result(self, score, correct_count, total_count, started_at):
        self.add_history(started_at, score, total_count, correct_count)
        
        print("\n\n========================================")
        if correct_count == 0:
            print("한 문제도 맞히지 못했습니다.")
            self.save_state()
            return
        
        print(f"🏆 결과: {total_count}문제 중 {correct_count}문제 정답! | {score}/{total_count * 2}점")
        if score > self.best_record["score"] or (score == self.best_record["score"] and total_count > self.best_record["total_count"]):
            print("🎉 새로운 최고 점수입니다! 최고 점수가 갱신되었습니다!")
            self.best_record = {
                "score": score,
                "total_count": total_count,
                "best_count": correct_count
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
        
        hint = self.get_input_string(
            prompt="힌트를 입력하세요: ",
            empty_message="힌트는 비어있을 수 없습니다. 다시 입력해주세요.",
            cancel_message="\n퀴즈 추가가 취소되었습니다. 메뉴로 돌아갑니다.\n",
            return_none=True
        )
        if hint is None:
            return
        
        new_quiz = Quiz(question, choices, answer, hint)
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

    def delete_quiz(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 0개이므로 삭제가 불가합니다.\n")
            return
        min_value = 1
        max_value = len(self.quizzes)
        
        print("\n퀴즈 삭제를 시작합니다.\n")
        self.view_quiz_list()
        
        user_input = self.get_input_number(
            f"삭제 번호({min_value}-{max_value}): ",
            min_value=min_value,
            max_value=max_value,
            empty_message=f"입력이 비어있습니다. {min_value}-{max_value} 사이의 문제 번호를 입력해주세요.",
            invalid_message=f"잘못된 입력입니다. {min_value}-{max_value} 사이의 문제 번호를 입력해주세요.",
            cancel_message="\n사용자에 의해 퀴즈 삭제를 중단합니다.",
            return_none=True
        )
        if user_input is None:
            return
        removed = self.quizzes.pop(user_input-1)
        self.save_state()
        print(f"'[{user_input}] {removed.question}' 문제를 삭제하였습니다.")
        print(f"남은 문제는 {len(self.quizzes)}개입니다.")