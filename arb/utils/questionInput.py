

class QuestionInput:
    
    @staticmethod
    def realize(question):
        print(question)
        decision = input()
        print(f"Usted decidió {decision}")
        return (decision.lower() == 's')