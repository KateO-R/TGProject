from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Hello!')],
    [KeyboardButton(text='Buy!')]
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='video', url='https://rutube.ru/shorts/200a7d5d5cdfb755628372e234430c58/?r=wd')],
    [InlineKeyboardButton(text='music', url='https://music.yandex.ru/genre/%D1%8D%D0%BC%D0%B1%D0%B8%D0%B5%D0%BD%D1%82')],
    [InlineKeyboardButton(text='news', url='https://dzen.ru/news')]
])

def show_more_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Show more', callback_data='show_more'))
    return keyboard.adjust(1).as_markup()

def options_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Option 1', callback_data='option_1'))
    keyboard.add(InlineKeyboardButton(text='Option 2', callback_data='option_2'))
    return keyboard.adjust(2).as_markup()
