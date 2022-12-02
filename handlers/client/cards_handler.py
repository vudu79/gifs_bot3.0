import random
from datetime import datetime
from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot import bot
from utils import func_chunk, phraze_list, StaticMedia
from keyboards import reply_keyboard_cards_builder

router = Router()

static_media = StaticMedia(stickers_url="static/stickers_tlgrm.json", calendar_url='calendar.json')


@router.message(text="Открытки", state=None)
async def cards_menu_show_handler(message: Message):
    # await message.answer(message.from_user.id,
    #                        "Более 10000 открыток на праздники!!!",
    #                        reply_markup=InlineKeyboardMarkup(row_width=2).row(
    #                            InlineKeyboardButton(text="Сегодня", callback_data="holiday__today_"),
    #                            InlineKeyboardButton(text="Календарь", callback_data="holiday__calendar_")))
    # await message.delete_reply_markup()
    await message.answer("Более 10000 открыток на праздники!!!",
                         reply_markup=reply_keyboard_cards_builder.as_markup(resize_keyboard=True))


@router.message(text="Календарь", state=None)
async def carendar_holiday_message_handler(message: Message):
    inline_keyboard_holiday_builder = InlineKeyboardBuilder()
    calendar_dict = static_media.get_calendar_dict()
    for month in calendar_dict.keys():
        # inline_keyboard_holiday.clean()
        inline_keyboard_holiday_builder.add(
            InlineKeyboardButton(text=f'{month}', callback_data=f'month__{month}'))
    inline_keyboard_holiday_builder.adjust(3)
    await message.answer('Выберите месяц...',
                         reply_markup=inline_keyboard_holiday_builder.as_markup(resize_keyboard=True))


@router.message(text="Сегодня", state=None)
async def today_holiday_message_handler(message: Message):
    inline_keyboard_today_events_builder = InlineKeyboardBuilder()

    today = datetime.today().strftime("%-d.%m")
    count = 0
    calendar_dict = static_media.get_calendar_dict()

    for month in calendar_dict.keys():
        event_list = calendar_dict[month].keys()
        for event in event_list:
            if event.startswith(today):
                count = count + 1
                # inline_keyboard_today_events.clean()
                inline_keyboard_today_events_builder.add(
                    InlineKeyboardButton(text=f'{event}', callback_data=f'&ev_{month}_{str(hash(event))}'))
        inline_keyboard_today_events_builder.adjust(3)

    if count > 0:
        await message.answer('Выберите праздник.',
                             reply_markup=inline_keyboard_today_events_builder.as_markup(resize_keyboard=True))
    else:
        await message.answer('На сегодня ничего не нашел ((')


@router.callback_query(text_startswith="month__", state=None)
async def show_month_events_callback_handler(collback: CallbackQuery):
    callback_user_id = collback.from_user.id
    month = collback.data.split("__")[1]
    calendar_dict = static_media.get_calendar_dict()
    events_list = calendar_dict[month].keys()

    inline_keyboard_events_builder = InlineKeyboardBuilder()
    for event in events_list:
        # inline_keyboard_events.clean()
        inline_keyboard_events_builder.add(
            InlineKeyboardButton(text=f'{event}', callback_data=f'&ev_{month}_{str(hash(event))}'))
    inline_keyboard_events_builder.adjust(1)
    await collback.message.answer('Все что нашел...',
                                  reply_markup=inline_keyboard_events_builder.as_markup(resize_keyboard=True))
    await collback.answer()


@router.callback_query(text_startswith="&ev_", state=None)
async def show_event_images_colaback_hendler(collback: types.CallbackQuery):
    # phraze_list = ["Склеиваю открытки...", "Ищу в интернетах...)", "Собираю пазл...",
    #                "Вспоминаю, что надо было сделать...", "Выгружаю по частям...", "Устал, у меня перерыв..."]
    callback_user_id = collback.from_user.id
    month = collback.data.split("_")[1]
    event_hash = collback.data.split("_")[2]

    # events_list = calendar_storage[month].keys()
    calendar_dict = static_media.get_calendar_dict()
    events_list = calendar_dict[month].keys()
    img_list = list()
    holiday = "???"

    for event in events_list:
        if event_hash == str(hash(event)):
            img_list = calendar_dict[month][event]
            holiday = event

    print(f'img_list - {img_list}')

    is_more_ten = bool

    len_img_list = len(img_list)
    print(f'len_img_list - {len_img_list}')
    len_generator = 0

    if len_img_list > 0:
        if len_img_list > 10:
            len_generator = (len_img_list // 10) + (0 if (len_img_list % 10) == 0 else 1)
            print(f'len_generator - {len_generator}')
            image_generator = func_chunk(img_list, 10)
            print(f'image_generator - {image_generator}')
            is_more_ten = True
        else:
            image_generator = (x for x in img_list)
            is_more_ten = False

        await collback.message.answer(f'Выбран праздник "{holiday.split("-")[1]}". Найдено {len_img_list} шт.')

        if is_more_ten:
            for x in range(len_generator):
                step_list = next(image_generator)
                await collback.message.answer(
                    f'{random.choice(phraze_list) if len_img_list > 10 else "Минутку, подбираю открытки..."}')
                # media = types.MediaGroup()
                media = list()
                for img in step_list:
                    if img != "":
                        # media.attach_photo(types.InputMediaPhoto(img), f'{holiday.split("-")[1]}')
                        media.append(types.InputMediaPhoto(type='photo', media=img))

                try:
                    await bot.send_media_group(callback_user_id, media=media)
                # except RetryAfter as e:
                #     await asyncio.sleep(e.timeout)
                except Exception as ee:
                    print(f'Что то пошло не так - {ee}')

        else:
            # media = types.MediaGroup()
            media = list()
            for img in image_generator:
                # media.attach_photo(types.InputMediaPhoto(img), f'{holiday.split("-")[1]}')
                media.append(types.InputMediaPhoto(type='photo', media=img))

            try:
                await bot.send_media_group(callback_user_id, media=media)
            # except RetryAfter as e:
            #     await asyncio.sleep(e.timeout)
            except Exception as ee:
                print(f'Что то пошло не так - {ee}')

        await collback.answer()

    await collback.answer("К сожалению, для этого праздника открыток нет.")
