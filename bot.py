# Объект бота
from aiogram import Bot, Dispatcher

from config_reader import config
from utils import StaticMedia

static_media = StaticMedia(stickers_url="static/stickers_tlgrm.json", calendar_url='calendar.json',
                           memes_url="static/half_memes.json")


bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
# bot = Bot(token="5788022696:AAG6Vw4Feolg4LPQybsU0iAUUaE_UqhwwtQ")
# Диспетчер
dp = Dispatcher()

