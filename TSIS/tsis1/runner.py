from connect import connect

conn = connect()
cursor = conn.cursor()


# TEST PROCEDURES
def test_add_phone():
    name = input("Введите имя контакта: ")
    phone = input("Введите новый номер: ")
    ptype = input("Тип (mobile/work/home) [mobile]: ") or "mobile"
    
    cursor.execute("CALL add_phone(%s, %s, %s)", [name, phone, ptype])
    conn.commit() 
    print(f"Номер {phone} добавлен для {name}")

def test_move_group():
    name = input("Кого переместить?: ")
    group = input("В какую группу?: ")
    
    cursor.execute("CALL move_to_group(%s, %s)", [name, group])
    conn.commit()
    print(f"Контакт {name} теперь в группе {group}")


# TEST FUNCTION
def test_search():
    pattern = input("Enter name to search: ") # Добавь эту строку
    cursor.callproc("search_contacts", [pattern]) # Передай pattern вместо "Alice"
    rows = cursor.fetchall()
    if not rows:
        print("No one found.")
    for r in rows:
        print(r)

while True:
    print("""
1. add_phone
2. move_to_group
3. search_contacts
4. exit
""")

    choice = input("> ")

    if choice == "1":
        test_add_phone()

    elif choice == "2":
        test_move_group()

    elif choice == "3":
        test_search()

    elif choice == "4":
        break


cursor.close()
conn.close()