import json

from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from create_bot import stickers_list
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

phraze_list = ["Секундочку, склеиваю фотки...", "минутку, ищу в интернетах...)", "Подождите, собираю пазл...",
               "Надо подождать, вспоминаю, что надо было сделать...", "Подождите,выгружаю по частям...",
               "Приходите попозже, устал, у меня перерыв...", "Минутку подождите, я форматирую ваши диски))"]


class StaticMedia:
    sticker_list: list
    sticker_dict: dict
    calendar_dict: dict
    stickers_url: str
    calendar_url: str

    def __init__(self, stickers_url: str, calendar_url: str):
        self.stickers_url = stickers_url
        self.calendar_url = calendar_url
        with open(self.stickers_url, "r", encoding="utf-8") as file:
            self.sticker_list = json.load(file)
        self.sticker_dict = {}
        for pack in self.sticker_list:
            self.sticker_dict[pack["name"]] = pack
        with open(self.calendar_url, 'r', encoding='utf-8') as f:
            js = f.read()
        self.calendar_dict = json.loads(js)

    def get_stickers_list(self):
        return self.sticker_list

    def get_stickers_dict(self):
        return self.sticker_dict

    def get_calendar_dict(self):
        return self.calendar_dict


# with open('calendar_storage.json', 'r', encoding='utf-8') as f:
#     js = f.read()

# calendar_storage = json.loads(js)

# "static/stickers_tlgrm.json"
# 'calendar.json'

# def get_stickers(count: int, massage: types.Message, img_list: list):
#     media = types.MediaGroup()
#     if len(img_list) <= 6:
#         for img in img_list:
#             media.attach_photo(types.InputMediaPhoto(img))
#     else:
#         for x in range(0, 5):
#             media.attach_photo(types.InputMediaPhoto(img_list[x]))
#
#     try:
#         if len(media.media) > 0:
#             print(f'Медиа группа - {len(media.media)} ')
#
#             await bot.send_message(message.from_user.id, f'<em>{random.choice(phraze_list)}</em>',
#                                    parse_mode="HTML")
#
#             await bot.send_media_group(message.from_user.id, media=media)
#             await bot.send_message(message.from_user.id, f'Стикеры <b>"{random_sticker_dict["name"]}"</b>',
#                                    parse_mode="HTML",
#                                    reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(
#                                        text="Добавить в телеграм", url=f'{random_sticker_dict["url"]}')))
#             count = count + 1
#     except Exception as ee:
#         print(f"Что то пошло не так {ee}")
#         with open("static/bad_pack.txt", 'a') as file:
#             file.write(random_sticker_dict["name"])
#

# await bot.send_message(message.from_user.id, "Что то пошло не так...")

class PagesCallbackFactory(CallbackData, prefix="CategorY__"):
    page: int
    category_name: str


def get_pagination_keyboard(page: int = 0, category_list: any = None) -> InlineKeyboardBuilder:
    keyboard_builder = InlineKeyboardBuilder()
    has_next_page = len(category_list) > page + 1

    if page != 0:
        keyboard_builder.add(
            InlineKeyboardButton(
                text="👈",
                callback_data=PagesCallbackFactory(page=page - 1,
                                                   category_name=f'{category_list[page - 1]["searchterm"]}').pack()
            )
        )

    keyboard_builder.add(
        InlineKeyboardButton(
            text=f'Показать все из "{str.capitalize(category_list[page]["searchterm"])}"',
            # callback_data=f'category__{category_list[page]["searchterm"]}"'
            callback_data=PagesCallbackFactory(category_name=f'{category_list[page + 1]["searchterm"]}').pack()
        )
    )

    if has_next_page:
        keyboard_builder.add(
            InlineKeyboardButton(
                text="👉",
                callback_data=PagesCallbackFactory(page=page + 1,
                                                   category_name=f'{category_list[page + 1]["searchterm"]}').pack()
            )
        )
    keyboard_builder.adjust(1)
    return keyboard_builder


def get_pagination_list(packs_count: int):
    res_list = list()
    count = packs_count % 100
    # print(count)
    last = 0
    if count > 0:
        for x in range(1, packs_count - 99, 100):
            last = x + 99
            res_list.append((x, last))
        res_list.append((last + 1, last + count))
    else:
        for x in range(1, packs_count, 100):
            last = x + 99
            res_list.append((x, last))
    return res_list


def func_chunk(lst, n):
    for x in range(0, len(lst), n):
        e_c = lst[x: n + x]

        if len(e_c) < n:
            e_c = e_c + ["" for y in range(n - len(e_c))]
        yield e_c
