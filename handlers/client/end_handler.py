import json
import string

from aiogram import Router
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message, ContentType
from aiogram.utils.markdown import italic, code, text

router = Router()


@router.message()
async def mat_filter_handler(message: Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('json_mat.files')))) != set():
        await message.reply("Маты запрещены в чате")
        await message.delete()


@router.message(content_types=ContentType.ANY)
async def unknown_message(msg: Message):
    message_text = text('Я не знаю, что с этим делать',
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help', 'и кнопки внизу))')
    await msg.reply(message_text)


@router.message(content_types=ContentType.TEXT)
async def any_handler(message: Message):
    await message.delete()
    await message.answer("Это бот для ленивых, тут все на кнопках))")
