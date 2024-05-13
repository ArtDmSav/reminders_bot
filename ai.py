from sqlite3 import DatabaseError

from openai import OpenAI

from celery1.tasks import schedule_reminder
from config.data import AI_API_KEY
from db.commit import write_remind, deactivate
from function.functions import extract_datetime_and_text, str_to_datetime

client = OpenAI(api_key=AI_API_KEY)


async def process_message(msg: str = "vsg", time_now: str = "str", chat_id: int = 474103257, username: str = "art",
                          first_name: str = "dm", last_name: str = "sav", language: str = "ru") -> str:
    # prompt = f"""
    #     The message "{msg}" contains instructions for the user to set a reminder. The message should follow the following pattern:
    #    "user message datetime = 'yyyy-MM-dd-hh-mm-ss'" where datetime = 'yyyy-MM-dd-hh-mm-ss' is the timestamp when the
    #    user sent the message. where yyyy is the year, MM is the month, dd is the day, hh is the hour, mm is the minutes, ss is the seconds
    #    Also, the received text is possible in different languages, and you need to respond in the language in which you received the text
    #
    #   Task:
    #   1. Determine the date and time of sending a reminder based on the user’s message; to do this, add the number of
    #    years, months, weeks, days, hours or minutes to the date and time at which the message was sent. You may also
    #     have to calculate based on the days of the week
    #   2. Extract the text that should be sent to the user as a reminder.
    #
    #   Format your answer like this:
    #   "yyyy-mm-dd-hh-mm-ss
    #   reminder text"
    # """

    # response = client.chat.completions.create(
    #     model="gpt-4-0125-preview",
    #     messages=[
    #         {"role": "system",
    #          "content": (
    #              "You are an assistant that extracts reminders from user messages. "
    #              "The message contains user instructions for setting a reminder. "
    #              "The message follows this pattern: 'user message datetime = \"%Y-%m-%d %H:%M:%S\"', "
    #              "where datetime = \"%Y-%m-%d %H:%M:%S\" is the timestamp of when the user sent the message,"
    #              "where %Y is the year, %m is the month, %d is the day, %H is the hour, %M is the minutes, %S is the "
    #              "seconds.\n\n"
    #              "Also, the received text is possible in different languages, and you need to respond in the language "
    #              "in which you received the text"
    #              "Task:\n"
    #              "1. 1. Determine the date and time of sending a reminder based on the user’s message; to do this, add"
    #              " the number of years, months, weeks, days, hours or minutes to the date and time at which the message"
    #              " was sent. You may also have to calculate based on the days of the week\n"
    #              "2. Extract the text that should be sent to the user as the reminder.\n\n"
    #              "Format your response like this:\n"
    #              "\"2024-05-07 14:30:00\n14:30, 07 May 2024\nreminder text\""
    #          )},
    #         {"role": "user", "content": f"{msg} datetime = {time_now}"}
    #     ],
    #     max_tokens=100
    # )

    # time_remainder, datetime_show, reminder_msg = await extract_datetime_and_text(response.choices[0].message.content)
    time_remainder, datetime_show, reminder_msg = "2024-05-07 14:30:00", "14:30, 07 May 2024", "text from bot"
    if time_remainder == "E":
        return "Произошла ошибка, попробуйте снова!"
    else:
        if 'E' == write_remind(chat_id, username, first_name, last_name, language,
                               time_now, time_remainder, msg, reminder_msg):
            return "Произошла ошибка, попробуйте снова!"
        else:
            try:
                datetime_reminder = await str_to_datetime(time_remainder)
                schedule_reminder(chat_id, reminder_msg, datetime_reminder, time_remainder)
            except BaseException as e:
                print(e)
                return "Произошла ошибка, попробуйте снова!"
            else:
                return f"Напоминание будет установлено на {datetime_show} {reminder_msg}."
