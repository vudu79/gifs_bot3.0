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
            command='Memes',
            description='Поиск мемов'
        ),
        BotCommand(
            command='Gifs',
            description='Поиск гифок'
        ),
        BotCommand(
            command='Stickers',
            description='Много стикеров'
        ),
        BotCommand(
            command='Cards',
            description='Открытки на праздники'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())