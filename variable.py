#1 example
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

#2 example
x = 5
y = "John"
print(x)
print(y)
#3 example
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

#4 example
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)

#5 example
def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)