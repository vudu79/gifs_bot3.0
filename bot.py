# Объект бота
from aiogram import Bot, Dispatcher

from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
# bot = Bot(token="5788022696:AAG6Vw4Feolg4LPQybsU0iAUUaE_UqhwwtQ")
# Диспетчер
dp = Dispatcher()

