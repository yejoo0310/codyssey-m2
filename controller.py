from datetime import datetime, timezone

from model import (
    BestRecord,
    MultipleChoiceQuiz,
    QuizHistory,
    QuizHistoryEntry,
    Quizzes,
)
from repository import (
    HistoryRepository,
    JsonLdFileHistoryRepository,
    JsonFileQuizRepository,
    JsonFileStateRepository,
    QuizRepository,
    StateRepository,
)
from view import ConsoleView
from vo import (
    Answer,
    Choices,
    Command,
    Hint,
    Question,
    QuizCount,
    QuizPlayCommand,
)


class QuizGame:
    def __init__(self, view: ConsoleView | None = None) -> None:
        self.quizzes = Quizzes()
        self.best_record = BestRecord()
        self.view = ConsoleView() if view is None else view
        self.state_repository: StateRepository = JsonFileStateRepository("state.json")
        self.quiz_repository: QuizRepository = JsonFileQuizRepository("quiz.json")
        self.default_quiz_repository: QuizRepository = JsonFileQuizRepository(
            "default-quiz.json"
        )
        self.history_repository: HistoryRepository = JsonLdFileHistoryRepository(
            "history.jsonld"
        )
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
        self, question: str, choices: list[str], answer: int, hint: str
    ) -> MultipleChoiceQuiz:
        choices_vo = Choices.from_texts(choices)
        return MultipleChoiceQuiz(
            Question(question),
            choices_vo,
            Answer(answer, choices_vo),
            Hint(hint),
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

        selected_count = self.get_selected_quiz_count()
        if selected_count is None:
            return

        selected_quizzes = self.quizzes.pick_random(selected_count)
        self.view.show_quiz_start(selected_count)

        current_score = 0
        history_entries: list[QuizHistoryEntry] = []
        played_at = self.current_time()

        for i, quiz in enumerate(selected_quizzes, start=1):
            self.view.show_quiz(quiz, i)
            hint_used = False

            while True:
                user_input = self.view.get_answer_input(quiz)

                if user_input is None:
                    self.save_history_if_needed(
                        self.build_history(
                            played_at,
                            selected_count,
                            current_score,
                            history_entries,
                            "aborted",
                        )
                    )
                    return

                if isinstance(user_input, QuizPlayCommand):
                    if user_input.is_show_hint():
                        self.view.show_hint(quiz.hint())
                        hint_used = True
                        continue
                    continue

                is_correct = quiz.is_correct(user_input)
                history_entries.append(
                    QuizHistoryEntry(
                        quiz.question(),
                        quiz.answer(),
                        user_input.value,
                        self.current_time(),
                        is_correct,
                        hint_used,
                    )
                )

                if is_correct:
                    self.view.show_correct_answer()
                    current_score += 1
                else:
                    self.view.show_incorrect_answer(quiz.answer_label())
                break

        self.save_history_if_needed(
            self.build_history(
                played_at,
                selected_count,
                current_score,
                history_entries,
                "completed",
            )
        )
        self.show_result(selected_count, current_score)

    def get_selected_quiz_count(self) -> int | None:
        while True:
            parsed_count = self.view.get_quiz_count(self.quizzes.count())
            if parsed_count is None:
                return None

            try:
                return QuizCount(parsed_count, self.quizzes.count()).value
            except ValueError as error:
                self.view.show_error_message(str(error))

    def show_result(self, total_count: int, score: int) -> None:
        is_new_best = self.best_record.update(total_count, score)
        if is_new_best:
            self.save_state()
        self.view.show_result(total_count, score, is_new_best)

    def current_time(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def build_history(
        self,
        played_at: str,
        total_count: int,
        correct_count: int,
        entries: list[QuizHistoryEntry],
        status: str,
    ) -> QuizHistory | None:
        if not entries:
            return None

        return QuizHistory(
            played_at,
            total_count,
            correct_count,
            entries,
            status,
        )

    def save_history_if_needed(self, history: QuizHistory | None) -> None:
        if history is None:
            return

        try:
            self.history_repository.save(history)
        except Exception:
            self.view.show_history_save_error()

    def add_quiz(self) -> None:
        while True:
            new_quiz_form = self.view.get_new_quiz_form()
            if new_quiz_form is None:
                return

            question, choices, answer, hint = new_quiz_form
            try:
                new_quiz = self.create_quiz(question, choices, answer, hint)
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
