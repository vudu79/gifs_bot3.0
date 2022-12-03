import asyncio

from aiogram import Router
from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot import bot
from keyboards import reply_keyboard_gifs_builder, inline_keyboard_lang_builder
from utils import get_categories_tenor_req, get_pagination_keyboard, get_category_list_tenor_req, PagesCallbackFactory, \
    trend_req, search_req, random_req, translate_req

router = Router()


class FSMSearch(StatesGroup):
    subj = State()
    limit = State()


# categories_callback = CallbackData("CategorY__", "page", "category_name")

category_list = get_categories_tenor_req()


@router.message(text="Гифки", state=None)
async def gifs_menu_show_handler(message: Message):
    # await bot.send_message(message.from_user.id,
    #                        "Более 10000 открыток на праздники!!!",
    #                        reply_markup=InlineKeyboardMarkup(row_width=2).row(
    #                            InlineKeyboardButton(text="Сегодня", callback_data="holiday__today_"),
    #                            InlineKeyboardButton(text="Календарь", callback_data="holiday__calendar_")))
    # await message.delete_reply_markup()
    await message.answer("Помогу найти гифки рызными способами))",
                         reply_markup=reply_keyboard_gifs_builder.as_markup(resize_keyboard=True))


@router.message(text="Популярные категории", state=None)
async def category_index_handler(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Все сразу", callback_data="collect_cat__yes"),
                InlineKeyboardButton(text="По одной", callback_data="collect_cat__no"))
    await message.answer("Показать все категории или по одной, но с превью?",
                         reply_markup=builder.as_markup(resize_keyboard=True))


@router.callback_query(text_startswith="collect_cat__")
async def show_type_category_callback_handler(collback: CallbackQuery):
    res = collback.data.split("__")[1]
    if res == "yes":
        inline_keyboard_category_builder = InlineKeyboardBuilder()
        for teg in category_list:
            # inline_keyboard_category_builder.clean()
            inline_keyboard_category_builder.add(
                InlineKeyboardButton(text=f'{teg["searchterm"]}', callback_data=f'category__{teg["searchterm"]}'))
        inline_keyboard_category_builder.adjust(3)
        await collback.message.answer(
            'В каждой категории по несколько вариантов популярных гифок. Нажмите на любую для просмотра.',
            reply_markup=inline_keyboard_category_builder.as_markup(resize_keyboard=True))
        await collback.answer()
    else:
        if res == "no":
            category_one = category_list[0]
            keyboard_builder = get_pagination_keyboard(category_list=category_list)  # Page: 0

            await bot.send_animation(
                chat_id=collback.message.chat.id,
                animation=category_one["image"],
                reply_markup=keyboard_builder.as_markup(resize_keyboard=True)
            )


@router.callback_query(PagesCallbackFactory.filter())
async def paginate_category_callback_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    category_one = category_list[page]
    keyboard = get_pagination_keyboard(page=page, category_list=category_list)

    await bot.send_animation(
        chat_id=query.from_user.id,
        animation=category_one["image"],
        reply_markup=keyboard
    )


@router.callback_query(text_startswith="category__", state=None)
async def show_list_category_colaback_hendler(collback: CallbackQuery):
    callback_user_id = collback.from_user.id
    res = collback.data.split("__")[1]
    await collback.answer(f'Выбрана категория {res}')
    gifs_from_tenor_list = get_category_list_tenor_req(res)
    for gif in gifs_from_tenor_list:
        # try:
        await bot.send_animation(callback_user_id, gif)
        # except RetryAfter as e:
        #     await asyncio.sleep(e.timeout)
    await collback.answer()


# Машина состояний для searchAPI________________________________________________________________________________________
# Запускаем машину состояния FSMAdmin хэндлером

@router.message(text="Найти по слову")
async def choose_lang_handler(message: Message):
    await message.answer("Выберите язык на котором будете писать запрос",
                         reply_markup=inline_keyboard_lang_builder.as_markup(resize_keyboard=True))


@router.callback_query(text_startswith="leng__", state=None)
async def colaback_hendler_lang_start_search(collback: CallbackQuery, state: FSMContext):
    res = collback.data.split("__")[1]
    print(f'Выбран язык - {res}')
    global leng_type
    global leng_phrase
    if res == "rus_":
        leng_type = "ru"
        leng_phrase = "русском языке"
        print(leng_type)
    elif res == "engl_":
        leng_type = "en"
        leng_phrase = "английском языке"
        print(leng_type)
    await state.set_state(FSMSearch.subj)
    await collback.answer()
    await bot.send_message(collback.from_user.id, f'Напишите ключевое слово поиска на {leng_phrase}')


# Выход из состояния
@router.message(state="*", commands='отмена')
@router.message(text=['отмена', 'Отменить поиск'], state="*")
async def cansel_state_search(maseege: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await maseege.reply("Ok, отменяем)")
    await maseege.answer("Что будем искать?)")


# Устанавливаем машину состояния в состояние приема фото и запрашиваем у пользователя файл
@router.message(FSMSearch.subj)
async def load_subj_sm_search(message: Message, state: FSMContext):
    await state.update_data(subj=message.text)
    await state.set_state(FSMSearch.limit)
    await message.answer(
        "Сколько найти? Максимальное количество - 1000 gifs. Пишите число, это например 1, 2, 22))")


# Устанавливаем машину состояния в состояние приема названия и запрашиваем у пользователя текст
@router.message(FSMSearch.limit)
async def load_limit_sm_search(message: Message, state: FSMContext):
    await state.update_data(limit=message.text)
    await message.answer("Okey, я запомнил. Произвожу поиск ...")
    data = await state.get_data()
    list_gifs = search_req(data["subj"], data["limit"], leng_type)
    for gif in list_gifs:
        await bot.send_animation(message.from_user.id, gif)
    await message.answer("Сделано, жду команд!")
    await state.clear()


# Машина состояний для randomAPI________________________________________________________________________________________

class FSMRandom(StatesGroup):
    subj = State()


@router.message(text="Случайная по слову", state=None)
async def cm_start_random(message: Message, state: FSMContext):
    await state.set_state(FSMRandom.subj)
    await message.answer("Напишите ключевое слово для поиска на английском языке")


@router.message(state="*", commands='отмена')
@router.message(text=['отмена', 'Отменить поиск'], state="*")
async def cansel_state_random(maseege: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await maseege.answer("Ok, отменяем)")
    await maseege.answer("Что будем искать?)")


@router.message(FSMRandom.subj)
async def load_subj_sm_random(message: Message, state: FSMContext):
    await state.update_data(subj=message.text)
    await message.answer("Okey, я запомнил. Произвожу поиск ...")
    data = await state.get_data()
    await bot.send_animation(message.from_user.id, random_req(data['subj']))
    await state.clear()
    await message.answer("Сделано, жду команд!")


# Машина состояний для translateAPI________________________________________________

class FSMTranslate(StatesGroup):
    phrase = State()


@router.message(text="Гифка под фразу", state=None)
async def cm_start_translate(message: Message, state: FSMContext):
    await state.set_state(FSMTranslate.phrase)
    await message.answer("Напишите любую фразу на английском языке")


@router.message(state="*", commands='отмена')
@router.message(text=['отмена', 'Отменить поиск'], state="*")
async def cansel_state_translate(maseege: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await maseege.reply("Ok, отменяем)")
    await maseege.answer("Что будем искать?)")


@router.message(FSMTranslate.phrase)
async def load_subj_sm_translate(message: Message, state: FSMContext):
    await state.update_data(phrase=message.text)
    await message.answer("Okey, я запомнил. Произвожу поиск ...")
    data = await state.get_data()
    await bot.send_animation(message.from_user.id, translate_req(data['phrase']))
    await state.clear()
    await message.answer("Сделано, жду команд!")


# trendAPI_________________________________________________________________

@router.message(text="Популярные гифки")
async def trand_api(message: Message):
    await message.answer("Минутку, произвожу поиск...")
    # global gifs
    gifs = trend_req()
    for item in gifs.items():
        await bot.send_animation(message.from_user.id, item[1])

    gifs.clear()
    await message.answer("Сделано, жду команд!")

#
# @router.callback_query(Text(startswith="save_"))
# async def colaback_hendler(collback: CallbackQuery):
#     res = collback.data.split("_")[1]
#     # dbase.save_gif(gifs[res])
#     # print(gifs[res])
#     await collback.answer("В разработке...")
