import calendar
from datetime import date
from datetime import datetime

import sqlalchemy.sql
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command

from GenericRepository import TableRepository
from database.database import engine as database
from database.database import Day_Report
from sqlalchemy.orm import Session
from sqlalchemy import Date

import keyboard
import text

router = Router()
month_nums = map(str, (1, 13))


class PersonReport(StatesGroup):
    month = State()
    day = State()
    meal = State()
    report_id = State()
    breakfast_id = State()
    lunch_id = State()
    dinner_id = State()


@router.message(Command("report"))
async def choose_report_month(msg: Message, state=FSMContext):
    await state.set_state(PersonReport.month)
    await msg.answer(text=text.choose_month.format(year=datetime.now().year),
                     reply_markup=await keyboard.get_month_keyboard())


@router.callback_query(PersonReport.month)
async def choose_report_day(msg: CallbackQuery, state=FSMContext):
    data = msg.data
    await state.update_data(month=data)
    await state.set_state(PersonReport.day)
    await msg.message.answer(
        text=text.choose_day.format(year=datetime.now().year, month=calendar.month_name[int(data)]),
        reply_markup=await keyboard.get_days_keyboard(data))


@router.callback_query(PersonReport.day)
async def choose_part_of_day(msg: CallbackQuery, state=FSMContext):
    await state.update_data(day=msg.data)
    data = await state.get_data()

    current_report = await get_report_by_date_and_id(date(datetime.now().year, int(data["month"]), int(data["day"])),
                                                     msg.from_user.id)
    if current_report is None:
        await state.set_state(PersonReport.meal)
        await msg.message.answer(
            text=text.no_report_variant.format(
                cur_date=date(datetime.now().year, int(data["month"]), int(data["day"])).strftime("%d-%m-%Y")),
            reply_markup=await keyboard.get_eat_time())
    else:
        await msg.message.answer(text="!!!")


@router.callback_query(PersonReport.meal)
async def add_report(msg: CallbackQuery, state=FSMContext):
    await state.update_data(meal=msg.data)
    res = await state.get_data()
    if res["meal"] == "Завтрак":
        await msg.message.answer(text="Завтрак!!!")
    elif res["meal"] == "Обед":
        await msg.message.answer(text="Обед!")
    elif res["meal"] == "Ужин":
        await msg.message.answer(text="Ужин!")
    else:

        data = await state.get_data()

        if ("breakfast_id" not in data):
            await state.set_state(PersonReport.breakfast_id)
            await state.update_data(breakfast_id=sqlalchemy.sql.null())
        if ("lunch_id" not in data):
            await state.set_state(PersonReport.lunch_id)
            await state.update_data(lunch_id=sqlalchemy.sql.null())
        if ("dinner_id" not in data):
            await state.set_state(PersonReport.dinner_id)
            await state.update_data(dinner_id=sqlalchemy.sql.null())

        data = await state.get_data()
        await state.clear()

        report = Day_Report(person_id=msg.from_user.id, breakfast_id=data["breakfast_id"], lunch_id=data["lunch_id"],
                            dinner_id=data["dinner_id"],
                            date=date(datetime.now().year, int(data["month"]), int(data["day"])))
        a = 0
        await save_report(report, msg.message)


async def get_report_by_date_and_id(date: datetime, id: int):
    with Session(autoflush=False, bind=database.engine) as db:
        repository = TableRepository(db=db, entity=Day_Report)
        current_report = repository.get_by_date_and_id(date, id)
        return current_report


async def save_report(report: Day_Report, msg: Message):
    with Session(autoflush=False, bind=database.engine) as db:
        repository = TableRepository(db=db, entity=Day_Report)
        repository.add(report)
    await msg.answer(text="Данные успешно сохранены")
