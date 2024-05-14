import pathlib
import sqlite3
from datetime import datetime

dir_path = pathlib.Path.cwd()
path = pathlib.Path(dir_path, 'db', 'reminders.db')


def write_remind(chat_id: int, username: str, first_name: str, last_name: str, language: str, time_now: str,
                 time_sql: datetime, msg: str, reminder_msg: str, time_zone=None) -> None:
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''
    INSERT INTO reminder (chat_id, username, first_name, last_name, language, 
                           wr_time, remind_time, msg, reminder_msg, time_zone)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (chat_id, f'{username}', f'{first_name}', f'{last_name}', f'{language}', f'{time_now}', f'{time_sql}',
          f'{msg}', f'{reminder_msg}', time_zone))

    conn.commit()
    conn.close()
