class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer
    
    def display(self, index):
        print("\n----------------------------------------")
        print(f"[문제 {index}]")
        print(f"{self.question}\n")
        for i, c in enumerate(self.choices):
            print(f"{i+1}. {c}")


    def is_correct(self, user_input):
        return self.answer == user_input
    
    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer 
        }