from models import Quiz
from controller import QuizGame

def main():
    q1 = Quiz("1 + 1은?", ["1", "2", "3", "4"], 2)

    q1.display(1)

    user_ans = int(input("정답 입력: "))
    if (q1.is_correct(user_ans)):
        print("ans")
    else:
        print("no")
    
    qg1 = QuizGame()
    qg1.run()

if __name__ == "__main__":
    main()