from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Зарегистрироваться", callback_data="register")
    keyboard_builder.button(text="Войти", callback_data="sign in")
    return keyboard_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)


def get_diabet_type_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="1 тип диабета", callback_data="first type diabetes")
    keyboard_builder.button(text="2 тип диабета", callback_data="second type diabetes")
    keyboard_builder.button(text="Гестационный диабет", callback_data="Gestational diabetes")
    keyboard_builder.button(text="Специфический диабет", callback_data="Specific diabetes")
    return keyboard_builder.adjust(2).as_markup(one_time_keyboard=True, resize_keyboard=True)
