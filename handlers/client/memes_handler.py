import random
import re
from aiogram import Router, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot import bot
from keyboards.slient_kb import reply_keyboard_mems_builder
from utils import StaticMedia, get_pagination_list, phraze_list
from keyboards import reply_keyboard_stickers_builder
from bot import static_media
from utils.db_connect import Request

router = Router()


@router.message(text="Мемы")
async def stickers_menu_show_handler(message: Message):
    await message.answer("Много фото-мемов сваленных в одну кучу))",
                         reply_markup=reply_keyboard_mems_builder.as_markup(resize_keyboard=True))


@router.message(Command(commands='memes'))
async def stickers_menu_show_handler(message: Message):
    await message.answer("Много фото-мемов сваленных в одну кучу))",
                         reply_markup=reply_keyboard_mems_builder.as_markup(resize_keyboard=True))


@router.message(text='Случайные из кучи')
async def stickers_random_handler(message: Message, request: Request):
    memes_list = await request.select_all_memes()
    mem_url = random.choice(memes_list)
    bot.send_photo(message.from_user.id, mem_url)
    await message.answer("Случайные")



@router.message(text="Свежие и не очень мемы")
async def stickers_search_handler(message: Message, state: FSMContext):
    await message.answer("Свежие")

