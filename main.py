import asyncio
import contextlib
import logging

import psycopg_pool

from bot import dp, bot
from handlers.client import stickers_handler, start_handler, gifs_handler, cards_handler, end_handler, memes_handler
from middleware.db_session import DbSession

# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                    )


def create_pool():
    return psycopg_pool.AsyncConnectionPool(
        f'host=127.0.0.1 port=5432 dbname=bot_db user=andrey password=SpkSpkSpk1979 connect_timeout=60')


# Запуск процесса поллинга новых апдейтов
async def main():
    pool_connect = create_pool()
    dp.update.middleware(DbSession(pool_connect))

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
