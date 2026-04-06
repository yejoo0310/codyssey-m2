from models import Quiz
import os

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.file_path = "state.json"
        # self.load_data()
    
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
                    # self.save_state()
                    break
        except (KeyboardInterrupt, EOFError):
            print("사용자에 의해 프로그램이 강제 종료되었습니다.")
            #self.save_state()