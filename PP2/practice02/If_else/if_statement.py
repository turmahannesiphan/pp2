a = 33
b = 200
if b > a:
  print("b is greater than a")


number = 15
if number > 0:
  print("The number is positive")


is_logged_in = True
if is_logged_in:
  print("Welcome back!")


a1 = 200
b1 = 33
c1 = 500
if a1 > b1 and c1 > a1:
  print("Both conditions are True")

a2 = 200
b2 = 33
c2 = 500
if a2 > b2 or a2 > c2:
  print("At least one of the conditions is True")


a3 = 33
b3 = 200
if not a3 > b3:
  print("a3 is NOT greater than b3")


x = 41

if x > 10:
  print("Above ten,")
  if x > 20:
    print("and also above 20!")
  else:
    print("but not above 20.")


value = 50

if value < 0:
  print("Negative value")
elif value == 0:
  pass  # Zero case - no action needed
else:
  print("Positive value")