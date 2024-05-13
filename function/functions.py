import re
from datetime import datetime


async def extract_datetime_and_text(message: str) -> tuple:
    lines = message.splitlines()
    if len(lines) > 2:
        time = lines[0].strip()
        time_show = lines[1].strip()
        reminder_text = lines[2].strip()
    else:
        time = "E"

    return time, time_show, reminder_text


async def str_to_datetime(time_remainder: str) -> object:

    date_format = "%Y-%m-%d %H:%M:%S"
    datetime_obj = datetime.strptime(time_remainder, date_format)

    return datetime_obj
