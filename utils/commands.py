from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='cancel',
            description='Сбросить'
        ),
        BotCommand(
            command='Мемы',
            description='Поиск мемов в интернете'
        ),
        BotCommand(
            command='Гифки',
            description='Поиск гиф анимаций и картинок'
        ),
        BotCommand(
            command='Стикеры',
            description='Неприлично много стикеров'
        ),
        BotCommand(
            command='Открытки',
            description='Открытки на популярные праздники'
        ),




    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())