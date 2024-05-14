import pathlib
import sqlite3
from sqlite3 import OperationalError

from db.create import create_db

dir_path = pathlib.Path.cwd()
path = pathlib.Path(dir_path, 'db', 'reminders.db')


def time_zone_check(chat_id: int) -> int:
    create_db()

    conn = sqlite3.connect(path)
    try:
        c = conn.cursor()

        c.execute("""
        SELECT time_zone
        FROM reminder
        WHERE chat_id = ?
        ORDER BY id DESC
        LIMIT 1;
        """, (chat_id,))

        result = c.fetchone()
        c.close()
    except OperationalError:
        return 0

    if result:
        time_zone = result[0]
        return time_zone
    else:
        return 0
