from aiogram import Router
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message

from keyboards import reply_keyboard_main_builder
from utils.db_connect import Request
from datetime import datetime

router = Router()


@router.message(commands=['start', 'help'])
async def start_handler(message: Message, request: Request):
    user_login_time = str(datetime.utcnow().time())
    await request.add_user(message.from_user.id, message.from_user.first_name, message.chat.id, user_login_time)
    await message.answer(f'Привет, {message.from_user.first_name}!')
    await message.answer('Это бот для поиска полезного и не очень медиа в интернете.',
                         reply_markup=reply_keyboard_main_builder.as_markup(resize_keyboard=True))
    await message.answer("Что будем искать?")
    await message.answer("Тыц 👇")


@router.message(text="Меню")
async def main_menu_handler(message: Message):
    # await message.answer(message.from_user.id, "", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("...", reply_markup=reply_keyboard_main_builder.as_markup(resize_keyboard=True))
