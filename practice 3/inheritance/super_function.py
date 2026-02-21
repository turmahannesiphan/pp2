class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

class Student(Person):
  # Added 'year' to the parameters here
  def __init__(self, fname, lname, year): 
    super().__init__(fname, lname)
    self.graduationyear = year # Now 'year' is defined!

  def welcome(self):
    print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)

# Now this call works perfectly
x = Student("Mike", "Olsen", 2019)
x.printname()
print(x.graduationyear)
x.welcome()