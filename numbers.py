#1 example
x = 1
y = 35656222554887711
z = -3255522

print(type(x))
print(type(y))
print(type(z))
#2 example
x = 1.10
y = 1.0
z = -35.59

print(type(x))
print(type(y))
print(type(z))
#3 example
x = 35e3
y = 12E4
z = -87.7e100

print(type(x))
print(type(y))
print(type(z))
#4 example
x = 1    
y = 2.8  
z = 1j   


a = float(x)

b = int(y)

c = complex(x)

print(a)
print(b)
print(c)

print(type(a))
print(type(b))
print(type(c))
#5 example
import random

print(random.randrange(1, 67))