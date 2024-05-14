from datetime import datetime, timedelta

from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError


async def extract_datetime_and_text(message: str) -> tuple:
    lines = message.splitlines()

    if len(lines) > 1:
        time = lines[0].strip()
        reminder_text = lines[1].strip()
    else:
        time = "E"
        reminder_text = "E"

    return time, reminder_text


async def str_to_datetime(time_remainder: str) -> datetime:
    date_format = "%Y-%m-%d %H:%M:%S"
    datetime_obj = datetime.strptime(time_remainder, date_format)

    return datetime_obj


async def get_utc_offset(timezone_str: str):
    try:
        tz = timezone(timezone_str)
    except UnknownTimeZoneError:
        tz = timezone("Europe/Samara")

    now = datetime.now(tz)
    utc_offset = now.utcoffset()
    seconds_offset = int(utc_offset.total_seconds())

    return seconds_offset


async def datetime_to_sec(dt: datetime) -> int:
    seconds_offset = int(dt.timestamp())

    return seconds_offset


async def get_user_remainder_time(time: str, int_sec_offset: int) -> str:
    months = {
        1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
        7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    }

    dt_time = await str_to_datetime(time)

    if int_sec_offset > 0:
        time_remainder = dt_time + timedelta(seconds=int_sec_offset)
    else:
        time_remainder = dt_time - timedelta(seconds=abs(int_sec_offset))

    show_time_remainder = time_remainder.strftime(f'%H:%M, %d {months[time_remainder.month]} %Y')

    return show_time_remainder
