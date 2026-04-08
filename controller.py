from model import BestRecord, MultipleChoiceQuiz, Quizzes
from repository import QuizRepository, StateRepository
from view import ConsoleView
from vo import Answer, Choices, Command, Question


class QuizGame:
    def __init__(self, view: ConsoleView | None = None) -> None:
        self.quizzes = Quizzes()
        self.best_record = BestRecord()
        self.view = ConsoleView() if view is None else view
        self.state_repository = StateRepository("state.json")
        self.quiz_repository = QuizRepository("quiz.json")
        self.default_quiz_repository = QuizRepository("default-quiz.json")
        self.load_state()
    
    def run(self) -> None:
        try:
            while True:
                cmd = self.view.show_menu()
                if cmd is None:
                    continue

                if cmd.is_play_quiz():
                    self.play_quiz()
                elif cmd.is_add_quiz():
                    self.add_quiz()
                elif cmd.is_view_quiz_list():
                    self.view_quiz_list()
                elif cmd.is_show_best_score():
                    self.show_best_score()
                elif cmd.is_exit():
                    self.save_state()
                    break
        except (KeyboardInterrupt, EOFError):
            self.view.show_program_interrupted()
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
            self.view.show_state_reset()
            self.best_record = BestRecord()
        except Exception:
            self.view.show_state_reset()
            self.best_record = BestRecord()

    def load_quizzes(self) -> None:
        try:
            if not self.quiz_repository.exists():
                self.view.show_quiz_file_missing()
                self.restore_default_quizzes()
                return

            loaded_quizzes = self.quiz_repository.load()
            if loaded_quizzes.has_minimum(5):
                self.quizzes = loaded_quizzes
                self.view.show_quizzes_loaded()
                return

            self.view.show_not_enough_quizzes()
            self.restore_default_quizzes()
        except FileNotFoundError:
            self.view.show_quiz_file_missing()
            self.restore_default_quizzes()
        except ValueError:
            self.view.show_quiz_file_corrupted()
            self.restore_default_quizzes()
    
    def save_state(self) -> None:
        try:
            self.state_repository.save(self.best_record)
            self.quiz_repository.save(self.quizzes)
        except Exception:
            self.view.show_save_error()
    
    def play_quiz(self) -> None:
        if self.quizzes.is_empty() or not self.quizzes.has_minimum(5):
            self.view.show_no_quizzes_for_play()
            return

        self.view.show_quiz_start(self.quizzes.count())

        current_score = 0

        for i, quiz in enumerate(self.quizzes.items(), start=1):
            self.view.show_quiz(quiz, i)
            user_answer = self.view.get_answer_input(quiz)

            if user_answer is None:
                return
            
            if quiz.is_correct(user_answer):
                self.view.show_correct_answer()
                current_score += 1
            else:
                self.view.show_incorrect_answer(quiz.answer_label())
        
        self.show_result(current_score)

    def show_result(self, score: int) -> None:
        total_count = self.quizzes.count()
        is_new_best = self.best_record.update(total_count, score)
        if is_new_best:
            self.save_state()
        self.view.show_result(total_count, score, is_new_best)
            
    def add_quiz(self) -> None:
        while True:
            new_quiz_form = self.view.get_new_quiz_form()
            if new_quiz_form is None:
                return

            question, choices, answer = new_quiz_form
            try:
                new_quiz = self.create_quiz(question, choices, answer)
            except ValueError as error:
                self.view.show_error_message(str(error))
                continue

            self.quizzes.add(new_quiz)
            self.save_state()
            self.view.show_quiz_saved()
            return

    def view_quiz_list(self) -> None:
        self.view.show_quiz_list(self.quizzes)

    def show_best_score(self) -> None:
        self.view.show_best_record(self.best_record)
