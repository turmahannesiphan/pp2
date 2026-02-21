# *args — позволяет передавать любое количество позиционных аргументов

# 1. Доступ к элементам *args
def youngest_child(*kids):
    print("The youngest child is", kids[2])

youngest_child("Emil", "Tobias", "Linus")


# 2. Что такое *args на самом деле
def show_args(*args):
    print("Type:", type(args))
    print("First argument:", args[0])
    print("Second argument:", args[1])
    print("All arguments:", args)

show_args("Emil", "Tobias", "Linus")


# 3. Обычный аргумент + *args
def greet(greeting, *names):
    for name in names:
        print(greeting, name)

greet("Hello", "Emil", "Tobias", "Linus")


# 4. Сумма произвольного количества чисел
def sum_numbers(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_numbers(1, 2, 3))
print(sum_numbers(10, 20, 30, 40))
print(sum_numbers(5))


# 5. Поиск максимального числа
def max_number(*numbers):
    if len(numbers) == 0:
        return None

    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

print(max_number(3, 7, 2, 9, 1))


# **kwargs — позволяет передавать любое количество именованных аргументов (keyword arguments)

# 1. Простой пример с **kwargs
def show_last_name(**kid):
    print("His last name is", kid["lname"])

show_last_name(fname="Tobias", lname="Refsnes")


# 2. **kwargs — это словарь
def show_info(**info):
    print("Type:", type(info))
    print("Name:", info["name"])
    print("Age:", info["age"])
    print("All data:", info)

show_info(name="Tobias", age=30, city="Bergen")


# 3. Обычный аргумент + **kwargs
def user_profile(username, **details):
    print("Username:", username)
    print("Additional details:")
    for key, value in details.items():
        print(" ", key + ":", value)

user_profile("emil123", age=25, city="Oslo", hobby="coding")


# 4. Комбинация: обычный аргумент + *args + **kwargs
def full_info(title, *args, **kwargs):
    print("Title:", title)
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)

full_info("User Info", "Emil", "Tobias", age=25, city="Oslo")


# 5. Распаковка списка с помощью *
def add_numbers(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
result = add_numbers(*numbers)  # то же самое, что add_numbers(1, 2, 3)
print(result)


# 6. Распаковка словаря с помощью **
def greet(fname, lname):
    print("Hello", fname, lname)

person = {
    "fname": "Emil",
    "lname": "Refsnes"
}

greet(**person)  # то же самое, что greet(fname="Emil", lname="Refsnes")