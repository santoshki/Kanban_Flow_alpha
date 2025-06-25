import sqlite3

DATABASE = 'E:\\Entreprenuership\\PycharmProjects\\Kanban_Flow_alpha\\projects.db'


def read_projects():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # So you can access columns by name
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM projects")
    rows = cursor.fetchall()

    for row in rows:
        print(f"ID: {row['id']}, Name: {row['name']}, Description: {row['description']}, "
              f"POC: {row['poc']}, Start Date: {row['start_date']}, End Date: {row['end_date']}")

    conn.close()


if __name__ == "__main__":
    read_projects()