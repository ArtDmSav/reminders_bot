import asyncio
from telegram import Bot


async def main(txt=" Это твой бот"):
    bot = Bot(token='6702527387:AAEXUFTZJwjQOSpHQSrliQAOg0WLoSbcZ0k')
    await bot.send_message(chat_id=474103257, text=txt)

asyncio.run(main())
