import asyncio

from telegram import Bot


async def main(chat_id, message, bot_token):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=f'Привет, ты просил напомнить: {message}')


if __name__ == "__main__":
    asyncio.run(main())
