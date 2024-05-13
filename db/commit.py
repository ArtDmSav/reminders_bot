import sqlite3
import pathlib


dir_path = pathlib.Path.cwd()
path = pathlib.Path(dir_path, 'db', 'reminders.db')


def write_remind(chat_id: int, username: str, first_name: str, last_name: str, language: str, time_now: str,
                 time_sql: str, msg: str, reminder_msg: str, active=1):

    conn = sqlite3.connect(path)
    try:
        c = conn.cursor()

        c.execute('''
        INSERT INTO reminder (chat_id, username, first_name, last_name, language, 
                               wr_time, remind_time, msg, reminder_msg, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (chat_id, f'{username}', f'{first_name}', f'{last_name}', f'{language}', f'{time_now}', f'{time_sql}',
              f'{msg}', f'{reminder_msg}', active))

    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
        return "E"
    except sqlite3.OperationalError as e:
        print(f"OperationalError: {e}")
        return "E"

    except sqlite3.ProgrammingError as e:
        print(f"ProgrammingError: {e}")
        return "E"
    except sqlite3.DataError as e:
        print(f"DataError: {e}")
        return "E"
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError: {e}")
        return "E"

    else:
        conn.commit()
    finally:
        conn.close()


def deactivate(chat_id, time_remainder):

    conn = sqlite3.connect(path)
    try:
        c = conn.cursor()

        c.execute("""
        UPDATE reminder
        SET active = 0
        WHERE chat_id = ? AND remind_time = ?
        """, (chat_id, time_remainder))

    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
        return "E"
    except sqlite3.OperationalError as e:
        print(f"OperationalError: {e}")
        return "E"

    except sqlite3.ProgrammingError as e:
        print(f"ProgrammingError: {e}")
        return "E"
    except sqlite3.DataError as e:
        print(f"DataError: {e}")
        return "E"
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError: {e}")
        return "E"

    else:
        conn.commit()
    finally:
        conn.close()
