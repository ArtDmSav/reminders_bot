import pathlib
import sqlite3

dir_path = pathlib.Path.cwd()
path = pathlib.Path(dir_path, 'db', 'reminders.db')


def create_db() -> None:
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reminder (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        language TEXT,
        wr_time TEXT,
        remind_time TEXT,
        msg TEXT,
        reminder_msg TEXT,
        time_zone INTEGER
    )
    ''')

    conn.commit()
    conn.close()
