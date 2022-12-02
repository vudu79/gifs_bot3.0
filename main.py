import asyncio
import json
import logging
from aiogram import types

from bot import dp, bot
from handlers.client import stickers_handler, start_handler, gifs_handler, cards_handler, end_handler

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_router(start_handler.router)

    dp.include_router(stickers_handler.router)
    dp.include_router(cards_handler.router)
    dp.include_router(gifs_handler.router)

    dp.include_router(end_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # print(config.bot_token.get_secret_value())
    asyncio.run(main())
