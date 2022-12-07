import asyncio
import contextlib
import logging

from bot import dp, bot
from handlers.client import stickers_handler, start_handler, gifs_handler, cards_handler, end_handler, memes_handler

# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                    )


# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_router(start_handler.router)

    dp.include_router(memes_handler.router)
    dp.include_router(stickers_handler.router)
    dp.include_router(cards_handler.router)
    dp.include_router(gifs_handler.router)

    dp.include_router(end_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
