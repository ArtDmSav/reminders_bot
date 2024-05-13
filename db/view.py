import sqlite3
import pathlib


dir_path = pathlib.Path.cwd()
path = pathlib.Path(dir_path, 'db', 'reminders.db')


def fetch_reminders():
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id, reminder_msg FROM reminders WHERE remind_time <= datetime('now')")
    reminders = cursor.fetchall()
    conn.close()
    return reminders
