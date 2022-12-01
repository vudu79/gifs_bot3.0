from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

cansel_btn = KeyboardButton(text='Отменить поиск')
main_menu_button = KeyboardButton(text='Меню')

gifs_btn = KeyboardButton(text='Гифки')
cards_btn = KeyboardButton(text='Открытки')
mems_btn = KeyboardButton(text='Мемы')
stickers_btn = KeyboardButton(text='Стикеры')
help_btn = KeyboardButton(text='Помощь')

reply_keyboard_main_builder = ReplyKeyboardBuilder()
reply_keyboard_main_builder.row(gifs_btn, stickers_btn).row(cards_btn, mems_btn).row(help_btn)

search_btn = KeyboardButton(text='Найти по слову')
trend_btn = KeyboardButton(text='Популярные гифки')
random_btn = KeyboardButton(text='Случайная по слову')
translate_btn = KeyboardButton(text='Гифка под фразу')
category_btn = KeyboardButton(text='Популярные категории')
reply_keyboard_gifs_builder = ReplyKeyboardBuilder()
reply_keyboard_gifs_builder.row(category_btn, search_btn) \
    .row(random_btn, translate_btn) \
    .row(cansel_btn, trend_btn) \
    .row(main_menu_button)

calendar_btn = KeyboardButton(text='Календарь')
today_btn = KeyboardButton(text='Сегодня')
reply_keyboard_cards_builder = ReplyKeyboardBuilder()
reply_keyboard_cards_builder.row(today_btn, calendar_btn).row(main_menu_button)

random_btn = KeyboardButton(text='Случайные мемасы')
trend_btn = KeyboardButton(text='В тренде')
reply_keyboard_mems_builder = ReplyKeyboardBuilder()
reply_keyboard_mems_builder.row(random_btn, trend_btn).row(main_menu_button)

random_sticker_btn = KeyboardButton(text='Случайные паки')
search_sticker_btn = KeyboardButton(text='Поиск по словам')
search_all_sticker_btn = KeyboardButton(text='Показать все')
reply_keyboard_stickers_builder = ReplyKeyboardBuilder()
reply_keyboard_stickers_builder.row(search_all_sticker_btn).row(random_sticker_btn, search_sticker_btn).row(
    main_menu_button)

rus_button = InlineKeyboardButton(text="Русский", callback_data="leng__rus_")
english_button = InlineKeyboardButton(text="English", callback_data="leng__engl_")

inline_keyboard_lang_builder = InlineKeyboardBuilder()
inline_keyboard_lang_builder.row(rus_button, english_button)

all_names_inline_menu = InlineKeyboardMarkup(row_width=4)
