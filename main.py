from controller import QuizGame
from view import ConsoleView

def main() -> None:
    game = QuizGame(ConsoleView())
    game.run()

if __name__ == "__main__":
    main()
