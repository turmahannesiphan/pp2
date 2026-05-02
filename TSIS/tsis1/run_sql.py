import psycopg2
from connect import connect

conn = connect()
cursor = conn.cursor()

# Читаем функции
with open("functions.sql", 'r', encoding='utf-8') as f:
    functions_sql = f.read()
    cursor.execute(functions_sql)
    print("Successfully run functions.sql")

# Читаем процедуры
with open("procedures.sql", 'r', encoding='utf-8') as f:
    procedures_sql = f.read()
    cursor.execute(procedures_sql)
    print("Successfully run procedures.sql")

conn.commit()
cursor.close()
conn.close()