from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def keyboard():
    button_1 = KeyboardButton(text="Добавить книгу")
    button_2 = KeyboardButton(text="Удалить книгу")
    button_3 = KeyboardButton(text="Найти книгу")
    button_4 = KeyboardButton(text="Показать все книги")
    button_5 = KeyboardButton(text="Изменить статус")

    first_row = [button_1, button_2]
    second_row = [button_3, button_4, button_5]
    rows = [first_row, second_row]
    markup = ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)
    return markup


