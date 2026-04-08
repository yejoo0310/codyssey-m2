from model.quiz import Quiz
class MultipleChoiceQuiz(Quiz):
    def __init__(self, question_text, choice_list, answer_index):
        super().__init__(question_text, choice_list, answer_index)

    def display(self, index):
        print("\n----------------------------------------")
        print(f"[문제 {index}]")
        print(f"{self.question_text()}\n")
        for i, choice in enumerate(self.choice_texts(), start=1):
            print(f"{i}. {choice}")

    def is_correct(self, user_input):
        return self._answer_index.matches(user_input)
