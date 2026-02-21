#Multiple inheritance — это когда один класс наследуется сразу от нескольких родителей.
class Person:
    def speak(self):
        print("I can speak")

class Athlete:
    def train(self):
        print("I can train")

class StudentAthlete(Person, Athlete):
    pass
    #Python ищет слева направо Method Resolution Order

s = StudentAthlete()
s.speak()
s.train()



class A:
    def __init__(self):
        print("A init")

class B:
    def __init__(self):
        print("B init")

class C(A, B):
    def __init__(self):
        super().__init__()
        print("C init")

c = C()