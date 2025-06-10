
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
        db.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                poc TEXT,
                start_date TEXT,
                end_date TEXT
            )
        ''')
        db.commit()


def insert_project(name, description, poc, start_date, end_date):
    db = get_db()
    db.execute('''
        INSERT INTO projects (name, description, poc, start_date, end_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, description, poc, start_date, end_date))
    db.commit()
    print("Data inserted successfully!")
