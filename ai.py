from openai import OpenAI

from celery1.tasks import schedule_reminder
from config.data import AI_API_KEY, BOT_TOKEN
from db.commit import write_remind
from db.create import create_db
from function.functions import extract_datetime_and_text, str_to_datetime, get_user_remainder_time


async def process_message(msg: str, time_now: str, chat_id: int, username: str,
                          first_name: str, last_name: str, language: str, offset_time_sec: int) -> str:
    client = OpenAI(api_key=AI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system",
             "content": (
                 "Я помощник, который извлекает напоминания из сообщений и вычисляет время напоминания."
                 "Сообщение соответствует следующему шаблону:"
                 " <сообщение пользователя \n'datetime' = %Y-%m-%d %H:%M:%S"
                 "Задача:\n"
                 "1. Определить дату и время отправки напоминания: взять 'datetime' прибавить время на основе данных "
                 "указаных в сообщении пользователя.\n"
                 "2. Извлечь текст, который должен быть отправлен пользователю в качестве напоминания.\n\n"
                 "Отформатируйте свой ответ следующим образом:"
                 "'2024-05-14 14:30:00\nreminder text'"
             )},
            {"role": "user", "content": f"{msg} \n'datetime' = {time_now}"}
        ],
        max_tokens=100
    )

    time_str_remainder, reminder_msg = await extract_datetime_and_text(response.choices[0].message.content)

    time_remainder = await str_to_datetime(time_str_remainder)
    datetime_show = await get_user_remainder_time(time_str_remainder, offset_time_sec)
    if time_str_remainder == "E":
        return "Произошла ошибка, попробуйте снова!"
    else:
        create_db()
        if 'E' == write_remind(chat_id, username, first_name, last_name, language,
                               time_now, time_str_remainder, msg, reminder_msg, offset_time_sec):
            return "Произошла ошибка, попробуйте снова!"
        else:
            try:
                schedule_reminder(chat_id, reminder_msg, time_remainder, BOT_TOKEN)
            except BaseException as e:
                print(e)
                return "Произошла ошибка, попробуйте снова!"
            else:
                return f"Напоминание будет установлено на {datetime_show}: {reminder_msg}."
