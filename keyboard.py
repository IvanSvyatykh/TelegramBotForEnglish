import calendar, locale
from calendar import Calendar
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from datetime import datetime
from calendar import monthrange

locale.setlocale(locale.LC_ALL, 'ru_RU')


def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Зарегистрироваться", callback_data="register")
    keyboard_builder.button(text="Войти", callback_data="sign in")
    return keyboard_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)


def get_month_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    months = calendar.month_name[1:]

    for month in months:
        keyboard_builder.button(text=f"{month}", callback_data=f"{datetime.strptime(month, '%B')}")

    return keyboard_builder.adjust(2).as_markup(one_time_keyboard=True, resize_keyboard=True)


def get_days_keyboard(month):
    keyboard_builder = InlineKeyboardBuilder()

    num_days = calendar.monthrange(23, 11)[1]

    for day in range(1, 30):
        keyboard_builder.button(text=f"{day}", callback_data=f"{day}")

    return keyboard_builder.adjust(3).as_markup(one_time_keyboard=True, resize_keyboard=True)


def get_diabetes_type_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="1 тип диабета", callback_data="first type diabetes")
    keyboard_builder.button(text="2 тип диабета", callback_data="second type diabetes")
    keyboard_builder.button(text="Гестационный диабет", callback_data="Gestational diabetes")
    keyboard_builder.button(text="Специфический диабет", callback_data="Specific diabetes")
    return keyboard_builder.adjust(2).as_markup(one_time_keyboard=True, resize_keyboard=True)
