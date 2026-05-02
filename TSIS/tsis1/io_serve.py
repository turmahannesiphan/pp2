import json
import csv
from datetime import datetime
from phonebook import cursor, conn, get_group_id

def parse_date(d):
    if not d:
        return None
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except:
        return None


# EXPORT TO JSON
def export_to_json(filename="TSIS/TSIS1/contacts.json"):
    cursor.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
    """)

    contacts = cursor.fetchall()

    result = []

    for c in contacts:
        contact_id = c[0]

        cursor.execute("""
            SELECT number, type
            FROM phones
            WHERE contact_id = %s
        """, (contact_id,))

        phones = cursor.fetchall()

        result.append({
            "id": contact_id,
            "name": c[1],
            "email": c[2],
            "birthday": str(c[3]) if c[3] else None,
            "group": c[4],
            "phones": [
                {"number": p[0], "type": p[1]} for p in phones
            ]
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("Exported to JSON")


# IMPORT FROM JSON
def import_from_json(filename="TSIS/TSIS1/contacts.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        name = item["name"]

        cursor.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        exist = cursor.fetchone()

        if exist:
            print(f"{name} already exists")
            action = input("skip / overwrite: ").strip().lower()

            if action == "skip":
                continue

            if action == "overwrite":
                cursor.execute("DELETE FROM contacts WHERE id = %s", (exist[0],))

        group_id = get_group_id(item.get("group"))

        cursor.execute("""
            INSERT INTO contacts (name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (
            item["name"],
            item.get("email"),
            parse_date(item.get("birthday")),
            group_id
        ))

        contact_id = cursor.fetchone()[0]

        for phone in item.get("phones", []):
            cursor.execute("""
                INSERT INTO phones (contact_id, number, type)
                VALUES (%s, %s, %s)
            """, (
                contact_id,
                phone["number"],
                phone["type"]
            ))

    conn.commit()
    print("Imported from JSON")


# IMPORT FROM CSV (UPDATED)


def reading_csv(path: str = "C:/Users/never/OneDrive/Рабочий стол/pp2/TSIS/TSIS1/contacts.csv"):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            name  = row.get('name', '').strip()
            phone = row.get('phone', '').strip()

            if not name or not phone:
                print("Skipping incomplete row:", row)
                continue

            phone_type = row.get('type', 'mobile').strip().lower()
            if phone_type not in ("home", "work", "mobile"):
                phone_type = "mobile"

            email    = row.get('email', '').strip() or None
            birthday = parse_date(row.get('birthday', '').strip())
            group_name = row.get('group', '').strip()
            group_id = get_group_id(group_name)

            if group_id is None and group_name:
                print("Unknown group:", group_name)

            # ── SAVEPOINT чтобы не ломать всю транзакцию
            cursor.execute("SAVEPOINT sp")

            try:
                # ── Проверяем, есть ли уже контакт
                cursor.execute(
                    "SELECT id FROM contacts WHERE name = %s AND email IS NOT DISTINCT FROM %s",
                    (name, email)
                )
                existing = cursor.fetchone()

                if existing:
                    contact_id = existing[0]
                else:
                    cursor.execute(
                        "INSERT INTO contacts (name, email, birthday, group_id) "
                        "VALUES (%s, %s, %s, %s) RETURNING id",
                        (name, email, birthday, group_id)
                    )
                    contact_id = cursor.fetchone()[0]

                # ── Добавляем телефон
                cursor.execute(
                    "INSERT INTO phones (contact_id, number, type) "
                    "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (contact_id, phone, phone_type)
                )

            except Exception as e:
                cursor.execute("ROLLBACK TO SAVEPOINT sp")
                print("Error processing row:", row, "|", e)

    conn.commit()
    print("CSV import completed")




if __name__ == "__main__":
    reading_csv("contacts.csv")