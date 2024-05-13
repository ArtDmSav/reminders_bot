from celery1.celery_app import app
from telegram import Bot

from db import commit
# from config.data import BOT_TOKEN


@app.task(ignore_result=True)
def send_reminder(chat_id, message, time_remainder):

    print("inside send_reminder")
    bot = Bot(token='6702527387:AAEXUFTZJwjQOSpHQSrliQAOg0WLoSbcZ0k')
    bot.send_message(chat_id=chat_id, text=f"Привет, ты просил напомнить что в {message}")
    print("bot sent msg")
    commit.deactivate(chat_id, time_remainder)
    print("deactivate msg")


def schedule_reminder(chat_id, message, datetime_reminder, time_remainder):
    send_reminder.apply_async((chat_id, message, time_remainder), eta=datetime_reminder)
    print(datetime_reminder)


# @app.task(ignore_result=True)
# def send_reminder(chat_id, message, time_remainder):
#     from celery1.celery_config import app
#     from telegram import Bot
#
#     from config.data import BOT_TOKEN
#     from db.commit import deactivate
#
#     print("insaid send_reminder")
#     bot = Bot(token=BOT_TOKEN)
#     bot.send_message(chat_id=chat_id, text=f"Привет, ты просил напомнить что в {message}")
#     print("bot sent msg")
#     deactivate(chat_id, time_remainder)  # Придумать обработчик/уведомление ошибки
#     print("deactivate msg")
#
#
# def schedule_reminder(chat_id, message, datetime_reminder, time_remainder):
#     from celery1.celery_config import app
#
#     send_reminder.apply_async((chat_id, message, time_remainder), eta=datetime_reminder)
#     print(datetime_reminder)
