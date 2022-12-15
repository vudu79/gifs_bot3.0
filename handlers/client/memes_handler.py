import random

from aiogram import Router
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot import bot
from keyboards.slient_kb import reply_keyboard_mems_builder, reply_keyboard_count_mems_builder
from utils.db_connect import Request

router = Router()


@router.message(text="Мемы")
async def stickers_menu_show_handler(message: Message):
    await message.answer("Большое количестов визуальных мемов и прикольной графики",
                         reply_markup=reply_keyboard_mems_builder.as_markup(resize_keyboard=True))


@router.message(Command(commands='memes'))
async def stickers_menu_show_handler(message: Message):
    await message.answer("Большое количестов визуальных мемов и прикольной графики",
                         reply_markup=reply_keyboard_mems_builder.as_markup(resize_keyboard=True))


@router.message(text=['Случайные из кучи', 'Назад в меню мемов'])
async def stickers_random_handler(message: Message, request: Request):
    count_mems = await request.select_count_memes()
    await message.answer(
        f"Фото и анимационные мемы из 8 источников в интернете. Все свалено в одну кучу и хорошо перемешано. Сейчас в куче <b>{count_mems[0]} мемов</b>. Можно тыкать пока палец не отвалится))",
        reply_markup=reply_keyboard_count_mems_builder.as_markup(resize_keyboard=True))


@router.message(text_startswith ='🔀 ')
async def stickers_random_handler(message: Message, request: Request):
    memes_list = await request.select_all_memes()
    mess = message.text
    if mess.endswith('1️⃣'):
        mem_url = random.choice(memes_list)
        await message.delete()
        await bot.send_photo(message.from_user.id, mem_url[0])

    if mess.endswith('3️⃣'):
        mem_url = random.choices(memes_list, k=3)
        await message.delete()
        for x in mem_url:
            await bot.send_photo(message.from_user.id, x[0])


    if mess.endswith('5️⃣'):
        mem_url = random.choices(memes_list, k=5)
        await message.delete()
        for x in mem_url:
            await bot.send_photo(message.from_user.id, x[0])

    if mess.endswith('🔟'):
        mem_url = random.choices(memes_list, k=10)
        await message.delete()
        for x in mem_url:
            await bot.send_photo(message.from_user.id, x[0])


    # x1_btn = KeyboardButton(text='🔀 1️⃣')
    # x3_btn = KeyboardButton(text='🔀 3️⃣')
    # x5_btn = KeyboardButton(text='🔀 5️⃣')
    # x10_btn = KeyboardButton(text='🔀 🔟')


@router.message(text="Свежие и не очень мемы")
async def stickers_search_handler(message: Message, state: FSMContext):
    await message.answer("В разработке")
