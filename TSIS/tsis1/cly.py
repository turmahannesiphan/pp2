from phonebook import filtering, cursor, conn 

PAGE_SIZE = 5


def show_menu():
    print("""
========================
CONTACT MANAGER
========================
1. Filter by group
2. Search by email
3. Sort contacts
4. Paginated view
5. Exit
""")


# TASK 1. Filter by group 

def filter_by_group():
    group = input("Enter group (Family/Work/Friend/Other): ").strip()
    filtering(group_name=group)


# TASK 2. Search by email

def search_by_email():
    email = input("Enter email part (e.g. gmail): ").strip()
    filtering(email=email)


# TASK 3. Sort contacts

def sort_contacts():
    print("Sort by: name / birthday / date_added")
    sort_by = input("> ").strip().lower()

    if sort_by == "name":
        order = "c.name"
    elif sort_by == "birthday":
        order = "c.birthday"
    elif sort_by == "date_added":
        order = "c.created_at"
    else:
        print("Invalid sort option")
        return

    query = f"""
        SELECT c.id, c.name, c.email, c.birthday, c.created_at, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY {order}
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    for r in rows:
        print(r)

# TASK 4. Pagination 

def paginated_view():
    page = 0

    while True:
        offset = page * PAGE_SIZE

        cursor.execute("""
            SELECT c.id, c.name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY c.id
            LIMIT %s OFFSET %s
        """, (PAGE_SIZE, offset))

        rows = cursor.fetchall()

        if not rows:
            print("No more data")
            break

        print("\n--- PAGE", page + 1, "---")
        for r in rows:
            print(r)

        cmd = input("\n[n]ext / [p]rev / [q]uit: ").strip().lower()

        if cmd == "n":
            page += 1
        elif cmd == "p" and page > 0:
            page -= 1
        elif cmd == "q":
            break


def main():
    while True:
        show_menu()
        choice = input("Choose: ").strip()

        if choice == "1":
            filter_by_group()

        elif choice == "2":
            search_by_email()

        elif choice == "3":
            sort_contacts()

        elif choice == "4":
            paginated_view()

        elif choice == "5":
            print("Bye Bye")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()