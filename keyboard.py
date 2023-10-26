from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Зарегестрироваться", request_contact=True)
    keyboard_builder.button(text="Войти", request_contact=True)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
