from aiogram import Router
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message

from keyboards import reply_keyboard_main_menu

router = Router()



@router.message(commands=['start', 'help'])
async def start_handler(message: Message):
    await message.answer( f'Привет, {message.from_user.first_name}!')
    await message.answer('Это бот для поиска полезного и не очень медиа в интернете.',
                           reply_markup=reply_keyboard_main_menu)
    await message.answer( "Что будем искать?")
    await message.answer( "Тыц 👇")


@router.message(Text(equals="Меню", ignore_case=True))
async def main_menu_handler(message: Message):
    # await message.answer(message.from_user.id, "", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("...", reply_markup=reply_keyboard_main_menu)
