from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


cansel_btn = KeyboardButton(text='Отменить поиск')
main_menu_button = KeyboardButton(text='Меню')

gifs_btn = KeyboardButton(text='Гифки')
cards_btn = KeyboardButton(text='Открытки')
mems_btn = KeyboardButton(text='Мемы')
stickers_btn = KeyboardButton(text='Стикеры')
help_btn = KeyboardButton(text='Помощь')
reply_keyboard_main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard_main_menu.row(gifs_btn, stickers_btn).row(cards_btn, mems_btn).row(help_btn)

search_btn = KeyboardButton(text='Найти по слову')
trend_btn = KeyboardButton(text='Популярные гифки')
random_btn = KeyboardButton(text='Случайная по слову')
translate_btn = KeyboardButton(text='Гифка под фразу')
category_btn = KeyboardButton(text='Популярные категории')
reply_keyboard_gifs = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard_gifs.row(category_btn, search_btn) \
    .row(random_btn, translate_btn) \
    .row(cansel_btn, trend_btn) \
    .row(main_menu_button)

calendar_btn = KeyboardButton(text='Календарь')
today_btn = KeyboardButton(text='Сегодня')
reply_keyboard_cards = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard_cards.row(today_btn, calendar_btn).row(main_menu_button)

random_btn = KeyboardButton(text='Случайные мемасы')
trend_btn = KeyboardButton(text='В тренде')
reply_keyboard_mems = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard_mems.row(random_btn, trend_btn).row(main_menu_button)

random_sticker_btn = KeyboardButton(text='Случайные паки')
search_sticker_btn = KeyboardButton(text='Поиск по словам')
search_all_sticker_btn = KeyboardButton(text='Показать все')
reply_keyboard_stickers = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard_stickers.row(random_sticker_btn, search_sticker_btn).row(search_all_sticker_btn).row(main_menu_button)

inline_keyboard_lang = InlineKeyboardMarkup(row_width=2)
rus_button = InlineKeyboardButton(text="Русский", callback_data="leng__rus_")
english_button = InlineKeyboardButton(text="English", callback_data="leng__engl_")
inline_keyboard_lang.row(rus_button, english_button)

all_names_inline_menu = InlineKeyboardMarkup(row_width=4)