class MyClass:
  x = 5

print(MyClass)

p1 = MyClass()
print(p1.x)


class Person:
  pass


#Чертёж дома → класс
#Конкретный дом → объект

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def say_hello(self):
        print("Hello, my name is", self.name) 
#__init__ это функция которая запускается автоматически, когда ты создаёшь объект
#это сам объект
p1 = Person("Aruzhan", 18)
p2 = Person("Dana", 20)
print(p1.name)
print(p2.age)
p1.say_hello()



class Cat:
    def __init__(self, name):
        self.name = name

    def meow(self):
        print(self.name, "says meow")
cat1 = Cat("Barsik")
cat2 = Cat("Murka")

cat1.meow()
cat2.meow()