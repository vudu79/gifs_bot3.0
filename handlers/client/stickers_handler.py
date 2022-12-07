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
from utils import StaticMedia, get_pagination_list, phraze_list
from keyboards import reply_keyboard_stickers_builder

static_media = StaticMedia(stickers_url="static/stickers_tlgrm.files", calendar_url='calendar.files')


class FSMStickersRandom(StatesGroup):
    count = State()


class FSMStickersSearch(StatesGroup):
    word = State()
    count = State()


class StickersPaginateCallback(CallbackData, prefix="my"):
    start: int
    end: int
    page: int


# stickers_paginate_callback = CallbackData('action', 'start_end')

router = Router()


@router.message(text="Стикеры")
async def stickers_menu_show_handler(message: Message):
    # await bot.send_message(message.from_user.id,
    #                        "Более 10000 открыток на праздники!!!",
    #                        reply_markup=InlineKeyboardMarkup(row_width=2).row(
    #                            InlineKeyboardButton(text="Сегодня", callback_data="holiday__today_"),
    #                            InlineKeyboardButton(text="Календарь", callback_data="holiday__calendar_")))
    # await message.delete_reply_markup()
    await message.answer("Более 25000 стикер-паков!!! Найти бы только нужный((",
                         reply_markup=reply_keyboard_stickers_builder.as_markup(resize_keyboard=True))


@router.message(text="Случайные паки", state=None)
async def stickers_random_handler(message: Message, state: FSMContext):
    await message.answer("Сколько паков найти?")
    await state.set_state(FSMStickersRandom.count)


@router.message(text="Поиск по словам", state=None)
async def stickers_search_handler(message: Message, state: FSMContext):
    await message.answer("Введите слово или фразу для поиска (ru/en)...")
    await state.set_state(FSMStickersSearch.word)


@router.message(text="Показать все")
async def show_all_stickers_handler(message: Message):
    stickers_dict = static_media.get_stickers_dict()
    stickers_titles = list(stickers_dict.keys())
    stickers_titles_inline_builder = InlineKeyboardBuilder()

    paginate_inline_kb_builder = InlineKeyboardBuilder()

    paginate_list = get_pagination_list(len(stickers_titles))
    for num, page in enumerate(paginate_list):
        activ = "👉" if num == 1 else ""
        paginate_inline_kb_builder.add(InlineKeyboardButton(text=f'{activ}{num}',
                                                            callback_data=StickersPaginateCallback(
                                                                start=page[0],
                                                                end=page[1],
                                                                page=num).pack()))

    paginate_inline_kb_builder.adjust(8)

    for x in range(0, 99):
        stickers_titles_inline_builder.add(
            InlineKeyboardButton(text=f"{stickers_titles[x]}", url=f'{stickers_dict[stickers_titles[x]]["url"]}'))
    stickers_titles_inline_builder.adjust(3)
    await message.answer(f"Всего найдено - {len(stickers_dict.keys())}. На странице по 100 шт.",
                         reply_markup=stickers_titles_inline_builder.as_markup(resize_keyboard=True))

    await bot.send_message(message.from_user.id,
                           "и еще немного страниц...",
                           reply_markup=paginate_inline_kb_builder.as_markup(resize_keyboard=True))

    # global stickers_names_gen
    # for x in range(0, 50):
    #     name = next(stickers_names_gen)
    #     all_names_inline_menu.clean()
    #     all_names_inline_menu.add(InlineKeyboardButton(f'{name}', url=f'{stickers_dict[name]["url"]}'))
    #
    # await bot.send_message(message.from_user.id, f"Всего {len(stickers_dict.keys())} паков. Отправил первые 50 шт...",
    #                        reply_markup=all_names_inline_menu)
    # await bot.send_message(message.from_user.id, "{Хватит?}",
    #                        reply_markup=InlineKeyboardMarkup(row_width=2)
    #                        .row(InlineKeyboardButton("Продолжаем", callback_data="all_stick__yet"),
    #                             InlineKeyboardButton("Надоело", callback_data="all_stick__enough")))
    #


@router.callback_query(StickersPaginateCallback.filter())
async def all_stickers_pagination_callback_handler(callback: types.CallbackQuery,
                                                   callback_data: StickersPaginateCallback):
    stickers_dict = static_media.get_stickers_dict()
    stickers_titles = list(stickers_dict.keys())

    stickers_titles_inline_builder = InlineKeyboardBuilder()

    for x in range(callback_data.start, callback_data.end):
        stickers_titles_inline_builder.add(
            InlineKeyboardButton(text=f"{stickers_titles[x]}", url=f'{stickers_dict[stickers_titles[x]]["url"]}'))
    stickers_titles_inline_builder.adjust(3)
    await callback.message.answer(f"Страница - {callback_data.page}",
                                  reply_markup=stickers_titles_inline_builder.as_markup(resize_keyboard=True))

    paginate_inline_kb_builder = InlineKeyboardBuilder()
    paginate_list = get_pagination_list(len(stickers_titles))
    for num, page in enumerate(paginate_list):
        activ = "👉" if num == callback_data.page else ""
        paginate_inline_kb_builder.add(InlineKeyboardButton(text=f'{activ}{num}',
                                                            callback_data=StickersPaginateCallback(
                                                                start=page[0],
                                                                end=page[1],
                                                                page=num).pack()))
    paginate_inline_kb_builder.adjust(8)
    await bot.send_message(callback.message.chat.id, "...",
                           reply_markup=paginate_inline_kb_builder.as_markup(resize_keyboard=True))

    await callback.answer()


@router.message(FSMStickersSearch.word)
async def load_word_search_stickers(message: Message, state: FSMContext):
    stickers_dict = static_media.get_stickers_dict()
    stickers_titles = stickers_dict.keys()
    await state.update_data(word=message.text)
    data = await state.get_data()

    matches_list = list(filter(lambda x: data['word'] in x, stickers_titles))
    # await bot.send_message(message.from_user.id, f'{matches_list}')
    # for x in stickers_names:
    #     await bot.send_message(message.from_user.id, f'{x}')

    if len(matches_list) > 0:
        for name in matches_list:
            bold_name = name[:name.index(data['word'])] + \
                        "<b>" + data['word'].upper() + "</b>" \
                        + name[name.index(data['word'])
                               + len(data['word']):]

            # media = types.MediaGroup()
            media = list()
            img_list = stickers_dict[name]["stickers"]

            if len(img_list) <= 4:
                for img in img_list:
                    media.append(types.InputMediaPhoto(type='photo', media=img))
            else:
                for x in range(0, 3):
                    media.append(types.InputMediaPhoto(type='photo', media=img_list[x]))
            try:
                if len(media) > 0:
                    print(f'Медиа группа - {len(media)} ')

                    await bot.send_media_group(message.from_user.id, media=media)

                    builder = InlineKeyboardBuilder()
                    builder.row(InlineKeyboardButton(text="Подробней / Добавить в телеграм",
                                                     url=f'{stickers_dict[name]["url"]}'))

                    await bot.send_message(message.from_user.id, f'{bold_name}',
                                           parse_mode="HTML",
                                           reply_markup=builder.as_markup(resize_keyboard=True))
            except Exception as ee:
                await bot.send_message(message.from_user.id,
                                       "<em>Извините, нашел какую-то чепуху, показывать не буду...</em>",
                                       parse_mode="HTML")
                print(f"Что то пошло не так {ee}")
                with open("static/bad_pack1.txt", 'a') as file:
                    file.write(name)
    else:
        await bot.send_message(message.from_user.id, "По вашему запросу ничего не найдено")
    await state.clear()


@router.message(FSMStickersRandom.count)
async def load_count_random_stickers(message: Message, state: FSMContext):
    num_string = message.text
    if not (num_string.isnumeric() and num_string.isdigit() and re.match("[-+]?\d+$", num_string)):
        await bot.send_message(message.from_user.id, "Введите целое число")
    else:
        stickers_list = static_media.get_stickers_list()
        packs_count = int(num_string)
        await state.update_data(count=packs_count)

        count = 0
        await message.answer(f'Ок, работаю...')
        while count < packs_count:
            random_sticker_dict = random.choice(stickers_list)
            img_list = random_sticker_dict["stickers"]

            # media = types.MediaGroup()
            media = list()
            if len(img_list) <= 6:
                for img in img_list:
                    media.append(types.InputMediaPhoto(type='photo', media=img))
            else:
                for x in range(0, 5):
                    media.append(types.InputMediaPhoto(type='photo', media=img_list[x]))

            try:
                if len(media) > 0:
                    await bot.send_message(message.from_user.id, f'<em>{random.choice(phraze_list)}</em>',
                                           parse_mode="HTML")

                    await bot.send_media_group(message.from_user.id, media=media)

                    builder = InlineKeyboardBuilder()
                    builder.row(InlineKeyboardButton(text="Добавить в телеграм", url=f'{random_sticker_dict["url"]}'))
                    await bot.send_message(message.from_user.id,
                                           f'Стикеры <b>"{random_sticker_dict["name"]}"</b>',
                                           parse_mode="HTML",
                                           reply_markup=builder.as_markup(resize_keyboard=True))
                    count = count + 1
            except Exception as ee:
                await bot.send_message(message.from_user.id,
                                       "<em>Извините, нашел какую-то чепуху, показывать не буду...</em>",
                                       parse_mode="HTML")
                print(f"Что то пошло не так в рандомных паках --- {ee}")
                with open("static/bad_pack.txt", 'a') as file:
                    file.write(random_sticker_dict["name"])
        # await bot.send_message(message.from_user.id, "Что то пошло не так...")

        await state.clear()
