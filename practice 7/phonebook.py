import csv
from connect import get_connection

def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    phone VARCHAR(20)
                );
            """)
            conn.commit()

def upload_from_csv(file_path):
    with get_connection() as conn:
        with conn.cursor() as cur:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader) 
                for row in reader:
                    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", row)
            conn.commit()

def add_contact(name, phone):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
            conn.commit()

def find_contacts(search):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM contacts WHERE name ILIKE %s OR phone ILIKE %s", (f'%{search}%', f'%{search}%'))
            return cur.fetchall()

def delete_contact(name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
            conn.commit()

# --- Консольное меню ---
if __name__ == "__main__":
    create_table()
    while True:
        print("\n1. Загрузить CSV | 2. Добавить | 3. Поиск | 4. Удалить | 0. Выход")
        cmd = input("Выбор: ")
        if cmd == '1': upload_from_csv('contacts.csv'); print("Готово!")
        elif cmd == '2': add_contact(input("Имя: "), input("Тел: "))
        elif cmd == '3': 
            for r in find_contacts(input("Искать: ")): print(r)
        elif cmd == '4': delete_contact(input("Имя для удаления: "))
        elif cmd == '0': break