import calendar
from datetime import date
from datetime import datetime

import sqlalchemy.sql
from aiogram import Router, F
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
    breakfast = State()
    lunch = State()
    dinner = State()


@router.message(Command("report"))
async def choose_report_month(msg: Message, state=FSMContext):
    await state.set_state(PersonReport.month)
    await msg.answer(text=text.choose_month.format(year=datetime.now().year),
                     reply_markup=await keyboard.get_month_keyboard())


@router.message(Command("cancel"))
async def cancel_month(msg: Message, state=FSMContext):
    await state.clear()
    await msg.answer(text="Добавление отчета остановлено")


@router.callback_query(PersonReport.month)
async def choose_report_day(msg: CallbackQuery, state=FSMContext):
    data = msg.data
    await state.update_data(month=data)
    await state.set_state(PersonReport.day)
    await msg.message.answer(
        text=text.choose_day.format(year=datetime.now().year, month=calendar.month_name[int(data)]),
        reply_markup=await keyboard.get_days_keyboard(data))


@router.message(Command("back"), PersonReport.day)
async def back_to_month(msg: Message, state=FSMContext):
    await state.set_state(PersonReport.month)
    await msg.answer(text=text.choose_month.format(year=datetime.now().year),
                     reply_markup=await keyboard.get_month_keyboard())


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
        await set_state(current_report, state)
        await state.set_state(PersonReport.meal)
        await msg.message.answer(text=text.already_have_report.format(
            cur_date=date(datetime.now().year, int(data["month"]), int(data["day"])).strftime("%d-%m-%Y")),
            reply_markup=await keyboard.get_eat_time())


@router.message(Command("back"), PersonReport.meal)
async def back_to_month(msg: Message, state=FSMContext):
    await state.set_state(PersonReport.day)
    data = await state.get_data()
    await msg.answer(
        text=text.choose_day.format(year=datetime.now().year, month=calendar.month_name[int(data["month"])]),
        reply_markup=await keyboard.get_days_keyboard(data["month"]))


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
        await update_state(data, state)
        data = await state.get_data()
        await state.clear()

        if ("report_id" in data):
            await save_report(await update_data(await get_report_by_date_and_id(
                date(datetime.now().year, int(data["month"]), int(data["day"])),
                msg.from_user.id), data), msg.message)
        else:
            report = Day_Report(person_id=msg.from_user.id,
                                breakfast=data["breakfast"],
                                lunch=data["lunch"],
                                dinner=data["dinner"],
                                date=date(datetime.now().year, int(data["month"]), int(data["day"])))
            await save_report(report, msg.message)


async def update_state(data, state):
    if ("breakfast" not in data):
        await state.set_state(PersonReport.breakfast)
        await state.update_data(breakfast=sqlalchemy.sql.null())
    if ("lunch" not in data):
        await state.set_state(PersonReport.lunch)
        await state.update_data(lunch=sqlalchemy.sql.null())
    if ("dinner" not in data):
        await state.set_state(PersonReport.dinner)
        await state.update_data(dinner=sqlalchemy.sql.null())


async def update_data(current_report, data):
    current_report.breakfast = data["breakfast"]
    current_report.lunch = data["lunch"]
    current_report.dinner = data["dinner"]
    return current_report


async def get_report_by_date_and_id(date: datetime, id: int):
    with Session(autoflush=False, bind=database.engine) as db:
        repository = TableRepository(db=db, entity=Day_Report)
        current_report = repository.get_by_date_and_id(date, id)
        return current_report


async def set_state(current_report: Day_Report, state=FSMContext):
    await state.set_state(PersonReport.breakfast)
    await state.update_data(breakfast=current_report.breakfast)
    await state.set_state(PersonReport.lunch)
    await state.update_data(lunch=current_report.lunch)
    await state.set_state(PersonReport.dinner)
    await state.update_data(dinner=current_report.dinner)
    await state.set_state(PersonReport.report_id)
    await state.update_data(report_id=current_report.id)


async def save_report(report: Day_Report, msg: Message):
    with Session(autoflush=False, bind=database.engine) as db:
        repository = TableRepository(db=db, entity=Day_Report)
        repository.add(report)
    await msg.answer(text="Данные успешно сохранены")
