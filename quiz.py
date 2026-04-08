class Quiz:
    def __init__(self, question, choices, answer, hint):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint
    
    def display(self, index):
        print("\n----------------------------------------")
        print(f"[문제 {index}]")
        print(f"{self.question}\n")
        for i, c in enumerate(self.choices):
            print(f"{i+1}. {c}")


    def is_correct(self, user_input):
        return self.answer == user_input

    def calculate_score(self, user_input, hint_used):
        if not self.is_correct(user_input):
            return 0
        if hint_used:
            return 1
        return 2
    
    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }