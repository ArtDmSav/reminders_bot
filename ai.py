from openai import OpenAI

from celery1.tasks import schedule_reminder
from config.data import AI_API_KEY, BOT_TOKEN
from db.commit import write_remind
from db.create import create_db
from function.functions import extract_datetime_and_text, str_to_datetime


async def process_message(msg: str, time_now: str, chat_id: int, username: str,
                          first_name: str, last_name: str, language: str, offset_time_sec: int) -> str:
    client = OpenAI(api_key=AI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system",
             "content": ('''
            Я помощник, который извлекает напоминания из сообщений, вычисляет время напоминания для сервера и вычисляет
            время для вывода в меню пользователя с учетом его часового пояса. Сообщение соответствует следующему
            шаблону:

            <сообщение пользователя>
            'datetime' = %Y-%m-%d %H:%M:%S
            'offset' = %S

            Задача:
            1. Определить дату и время отправки напоминания:
                а) Если пользователь указал "ЧЕРЕЗ СКОЛЬКО НАПОМНИТЬ": прибавить это время к 'datetime'.
                б) Если пользователь указал ОПРЕДЕЛЕННОЕ ВРЕМЯ: отнять 'offset' время от "ОПРЕДЕЛЕНОЕ ВРЕМЯ".
            2. Определить дату и время отправки вывода в меню пользователя:
                а) Если упоминается "ЧЕРЕЗ СКОЛЬКО НУЖНО НАПОМНИТЬ", прибавить 'offset' к времени напоминания.
                б) Если указано ОПРЕДЕЛЕННОЕ ВРЕМЯ, то вывести ЕГО.
            3. Извлечь текст, который должен быть отправлен пользователю в качестве напоминания.
            
            После вычета времени возможно получить значения меньше 'datetime' или даже время прошлого дня, 
            это считать корректным поведение и выводить данное время согласно примеру ответа.
            
            Шаблон ответа:
            2024-05-14 15:30:00
            18:00 14 Май 2024
            покормить кота


            Сообщения содержат данные в указанном формате. Вычисли даты и времена для напоминания и вывода в меню 
            пользователя, а также извлеки текст напоминания.
            
            '''
                         )},
            {"role": "user", "content": f"{msg} \ndatetime = {time_now}\noffset = {offset_time_sec}"}
        ],
        max_tokens=100
    )

    time_str_remainder, time_show, reminder_msg = await extract_datetime_and_text(response.choices[0].message.content)
    print(f'{time_str_remainder} time remain\n{time_show} time show\n{reminder_msg}')
    time_remainder = await str_to_datetime(time_str_remainder)
    if time_str_remainder == "E":
        return "Произошла ошибка считывания данных, попробуйте снова!"
    else:
        create_db()
        if 'E' == write_remind(chat_id, username, first_name, last_name, language,
                               time_now, time_str_remainder, msg, reminder_msg, offset_time_sec):
            return "Произошла ошибка добавления данных, попробуйте снова!"
        else:
            try:
                schedule_reminder(chat_id, reminder_msg, time_remainder, BOT_TOKEN)
            except BaseException as e:
                return f"Произошла ошибка {e}, попробуйте снова!"
            else:
                return f"Напоминание будет установлено на {time_show}: {reminder_msg}."
