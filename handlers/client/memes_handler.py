import random
import re
from aiogram import Router, types
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

static_media = StaticMedia(stickers_url="static/stickers_tlgrm.files", calendar_url='calendar.files')


router = Router()


@router.message(text="Мемы")
async def stickers_menu_show_handler(message: Message):
    # await bot.send_message(message.from_user.id,
    #                        "Более 10000 открыток на праздники!!!",
    #                        reply_markup=InlineKeyboardMarkup(row_width=2).row(
    #                            InlineKeyboardButton(text="Сегодня", callback_data="holiday__today_"),
    #                            InlineKeyboardButton(text="Календарь", callback_data="holiday__calendar_")))
    # await message.delete_reply_markup()
    await message.answer("Более 900000 мемов!!!",
                         reply_markup=reply_keyboard_mems_builder.as_markup(resize_keyboard=True))


@router.message(text='Случайные мемасы')
async def stickers_random_handler(message: Message, state: FSMContext):
    await message.answer("Случайные")



@router.message(text="Свежие и не очень мемы")
async def stickers_search_handler(message: Message, state: FSMContext):
    await message.answer("Свежие")

