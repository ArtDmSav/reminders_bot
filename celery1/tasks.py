import asyncio

from celery1.celery_app import app
from .bot_send_message import main


@app.task(ignore_result=True)
def send_reminder(chat_id, message, bot_token) -> None:
    asyncio.run(main(chat_id, message, bot_token))


def schedule_reminder(chat_id, message, datetime_reminder, bot_token, ) -> None:
    send_reminder.apply_async((chat_id, message, bot_token), eta=datetime_reminder)
