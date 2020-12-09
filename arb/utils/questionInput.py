

class QuestionInput:
    
    @staticmethod
    def realize(question):
        print(question)
        decision = input()
        print(f"Usted decidió {decision}")
        return (decision.lower() == 's')

    @staticmethod
    def realizeNumberBicycle(question):
        print(question)
        decision = input()
        print(f"Usted eligió el bicicletero {decision}")
        return decision