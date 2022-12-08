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

router = Router()


@router.message(text="Мемы")
async def stickers_menu_show_handler(message: Message):
    await message.answer("Более 900000 мемов!!!",
                         reply_markup=reply_keyboard_mems_builder.as_markup(resize_keyboard=True))


@router.message(Command(commands='Гифки'))
async def stickers_menu_show_handler(message: Message):
    await message.answer("Более 900000 мемов!!!",
                         reply_markup=reply_keyboard_mems_builder.as_markup(resize_keyboard=True))


@router.message(text='Случайные мемасы')
async def stickers_random_handler(message: Message, state: FSMContext):
    await message.answer("Случайные")



@router.message(text="Свежие и не очень мемы")
async def stickers_search_handler(message: Message, state: FSMContext):
    await message.answer("Свежие")

