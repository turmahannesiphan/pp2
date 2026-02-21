class Person:
  def __init__(self, name, age = 0):
    self.name = name
    self.age = age

  def greet(self):
    print("Hello, my name is " + self.name)
  def get_info(self):
      return f"{self.name} is {self.age} years old"
  def celebrate_birthday(self):
    self.age += 1
    print(f"Happy birthday! You are now {self.age}")

p1 = Person("Emil")
p1.greet()
p2 = Person("Tobias", 28)
p2.celebrate_birthday()
print(p2.get_info())

del Person

class Calculator:
  def add(self, a, b):
    return a + b

  def multiply(self, a, b):
    return a * b

calc = Calculator()
print(calc.add(5, 3))
print(calc.multiply(4, 7))


class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def __str__(self):
    return f"{self.name} ({self.age})"

p1 = Person("Tobias", 36)
print(p1)