import sqlite3

db_name = "reminders.db"

conn = sqlite3.connect(db_name)
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
    active INTEGER(1)
)
''')


conn.commit()
conn.close()

