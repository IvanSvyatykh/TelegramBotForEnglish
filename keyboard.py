import calendar, locale
from calendar import Calendar
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from datetime import datetime
from datetime import date
from calendar import monthrange

locale.setlocale(locale.LC_ALL, 'ru_RU')


async def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Зарегистрироваться", callback_data="register")
    keyboard_builder.button(text="Войти", callback_data="sign in")
    return keyboard_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)


async def get_month_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    months = calendar.month_name[1:]

    for i in range(len(months)):
        keyboard_builder.button(text=f"{months[i]}", callback_data=f"{i + 1}")

    return keyboard_builder.adjust(2).as_markup(one_time_keyboard=True, resize_keyboard=True)


async def get_days_keyboard(month):
    keyboard_builder = InlineKeyboardBuilder()
    current_year = datetime.now().year
    num_days = monthrange(current_year, int(month))[1]
    days = [calendar.day_name[date(current_year, int(month), day).weekday()] for day in range(1, num_days + 1)]

    for i in range(len(days)):
        keyboard_builder.button(text=f"{days[i]}-{i + 1}", callback_data=f"{i + 1}")

    return keyboard_builder.adjust(3).as_markup(one_time_keyboard=True, resize_keyboard=True)


async def get_diabetes_type_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="1 тип диабета", callback_data="first type diabetes")
    keyboard_builder.button(text="2 тип диабета", callback_data="second type diabetes")
    keyboard_builder.button(text="Гестационный диабет", callback_data="Gestational diabetes")
    keyboard_builder.button(text="Специфический диабет", callback_data="Specific diabetes")
    return keyboard_builder.adjust(2).as_markup(one_time_keyboard=True, resize_keyboard=True)


async def get_eat_time():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Завтрак", callback_data="Завтрак")
    keyboard_builder.button(text="Обед", callback_data="Обед")
    keyboard_builder.button(text="Ужин", callback_data="Ужин")
    keyboard_builder.button(text="Сохранить", callback_data="Сохранить")
    return keyboard_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)


async def get_confirmation():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Сохранить", callback_data="Сохранить")
    keyboard_builder.button(text="Отмена", callback_data="Отмена")
    return keyboard_builder.adjust(2).as_markup(one_time_keyboard=True, resize_keyboard=True)
