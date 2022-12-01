import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from config_reader import config
from handlers import stickers_handler, start_handler, gifs_handler, cards_handler, end_handler

with open("static/stickers_tlgrm.json", "r", encoding="utf-8") as file:
    stickers_list = json.load(file)
stickers_dict = {}

for pack in stickers_list:
    stickers_dict[pack["name"]] = pack

with open('calendar.json', 'r', encoding='utf-8') as f:
    js = f.read()

calendar_dict = json.loads(js)

with open('calendar_storage.json', 'r', encoding='utf-8') as f:
    js = f.read()

calendar_storage = json.loads(js)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
# bot = Bot(token="5788022696:AAG6Vw4Feolg4LPQybsU0iAUUaE_UqhwwtQ")
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


def get_stickers():
    return stickers_list, stickers_dict


def get_calendar():
    return calendar_dict


# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_router(start_handler.router)

    dp.include_router(stickers_handler.router)
    dp.include_router(cards_handler.router)
    dp.include_router(stickers_handler.router)

    dp.include_router(end_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # print(config.bot_token.get_secret_value())
    asyncio.run(main())
