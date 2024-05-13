from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from ai import process_message
from config.data import BOT_TOKEN
from datetime import datetime


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Напишите мне напоминание.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    chat_id = update.effective_chat.id
    username = update.effective_user.username or "N/A"
    first_name = update.effective_user.first_name or "N/A"
    last_name = update.effective_user.last_name or "N/A"
    language = update.effective_user.language_code or "N/A"

    formatted_date_time = await process_message(user_message, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                chat_id, username, first_name, last_name, language)

    await update.message.reply_text(formatted_date_time)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()
