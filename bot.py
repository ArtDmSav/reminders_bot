from datetime import datetime

from pytz import timezone, utc
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from timezonefinder import TimezoneFinder

from ai import process_message
from config.data import BOT_TOKEN
from db.view import time_zone_check
from function.functions import get_utc_offset


async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [KeyboardButton(text="Отправить местоположение", request_location=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text('Пожалуйста, отправьте ваше местоположение для определения часового пояса, '
                                    'это важно для корректной работы бота!', reply_markup=reply_markup)


async def handle_location(update: Update, context: CallbackContext) -> None:
    user_location = update.message.location
    if user_location:
        tf = TimezoneFinder()
        user_tz = tf.timezone_at(lng=user_location.longitude, lat=user_location.latitude)
        context.chat_data['user_tz'] = user_tz

        if user_tz:
            user_time = datetime.now(timezone(user_tz)).strftime('%Y-%m-%d %H:%M:%S')
            await update.message.reply_text(f'Ваш часовой пояс: {user_tz}\nТекущее время: {user_time}\n\n'
                                            f'Напишите мне напоминание.')
        else:
            await update.message.reply_text(
                f'Не удалось определить ваш часовой пояс.\n Бот может работать некорректно!')
    else:
        await update.message.reply_text(f'Пожалуйста, отправьте ваше местоположение для корректной работы бота.')


async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    chat_id = update.effective_chat.id
    username = update.effective_user.username or "N/A"
    first_name = update.effective_user.first_name or "N/A"
    last_name = update.effective_user.last_name or "N/A"
    language = update.effective_user.language_code or "N/A"
    user_tz = context.chat_data.get('user_tz', 'N/A')

    if user_tz == 'N/A':
        user_tz = time_zone_check(chat_id)
    else:
        user_tz = await get_utc_offset(user_tz)
    formatted_date_time = await process_message(user_message, datetime.now(utc).strftime('%Y-%m-%d %H:%M:%S'),
                                                chat_id, username, first_name, last_name, language, user_tz)

    await update.message.reply_text(formatted_date_time)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()
