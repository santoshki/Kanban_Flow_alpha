import sqlite3
from flask import g

DATABASE = 'projects.db'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db()
        # Create projects table if it doesn't exist
        db.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                poc TEXT,
                start_date TEXT,
                end_date TEXT
            )
        ''')

        # Create tasks table if it doesn't exist, with start_date and assignee columns
        db.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT CHECK(status IN ('To Do', 'In Progress', 'Done')) DEFAULT 'To Do',
                priority TEXT CHECK(priority IN ('Low', 'Medium', 'High')) DEFAULT 'Medium',
                start_date TEXT,
                due_date TEXT,
                assignee TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            )
        ''')

        # Create comments table
        db.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                author TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
            )
        ''')

        # Migration: Add start_date column if missing
        try:
            db.execute("SELECT start_date FROM tasks LIMIT 1")
        except sqlite3.OperationalError:
            db.execute("ALTER TABLE tasks ADD COLUMN start_date TEXT")

        # Migration: Add assignee column if missing
        try:
            db.execute("SELECT assignee FROM tasks LIMIT 1")
        except sqlite3.OperationalError:
            db.execute("ALTER TABLE tasks ADD COLUMN assignee TEXT")

        db.commit()


def insert_project(name, description, poc, start_date, end_date):
    db = get_db()
    db.execute('''
        INSERT INTO projects (name, description, poc, start_date, end_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, description, poc, start_date, end_date))
    db.commit()
    print("Project inserted successfully!")


def insert_task(project_id, title, description, status, priority, start_date, due_date, assignee):
    db = get_db()
    db.execute('''
        INSERT INTO tasks (project_id, title, description, status, priority, start_date, due_date, assignee)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (project_id, title, description, status, priority, start_date, due_date, assignee))
    db.commit()


def update_task(task_id, title=None, description=None, status=None, priority=None, start_date=None, due_date=None, assignee=None):
    db = get_db()

    # Build dynamic update query depending on which params are provided
    fields = []
    params = []

    if title is not None:
        fields.append("title = ?")
        params.append(title)
    if description is not None:
        fields.append("description = ?")
        params.append(description)
    if status is not None:
        fields.append("status = ?")
        params.append(status)
    if priority is not None:
        fields.append("priority = ?")
        params.append(priority)
    if start_date is not None:
        fields.append("start_date = ?")
        params.append(start_date)
    if due_date is not None:
        fields.append("due_date = ?")
        params.append(due_date)
    if assignee is not None:
        fields.append("assignee = ?")
        params.append(assignee)

    params.append(task_id)

    if fields:
        query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
        db.execute(query, params)
        db.commit()


def get_tasks_for_project(project_id):
    db = get_db()
    return db.execute('SELECT * FROM tasks WHERE project_id = ?', (project_id,)).fetchall()