import calendar
from datetime import date
from datetime import datetime

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


@router.message(Command("report"))
async def choose_report_month(msg: Message, state=FSMContext):
    await state.set_state(PersonReport.month)
    await msg.answer(text=text.choose_month.format(year=datetime.now().year),
                     reply_markup=keyboard.get_month_keyboard())


@router.callback_query(PersonReport.month)
async def choose_report_day(msg: CallbackQuery, state=FSMContext):
    data = msg.data
    await state.update_data(month=data)
    await state.set_state(PersonReport.day)
    await msg.message.answer(
        text=text.choose_day.format(year=datetime.now().year, month=calendar.month_name[int(data)]),
        reply_markup=keyboard.get_days_keyboard(data))


@router.callback_query(PersonReport.day)
async def choose_part_of_day(msg: CallbackQuery, state=FSMContext):
    await state.update_data(day=msg.data)
    data = await state.get_data()
    await state.clear()

    current_report = await get_report_by_date(date(datetime.now().year, int(data["month"]), int(data["day"])))
    if current_report is None:
        await msg.message.answer(text="У вас еще нет отчетов за выбранную дату")
    else:
        await  msg.message.answer(text="!!!")


async def get_report_by_date(date: datetime):
    with Session(autoflush=False, bind=database.engine) as db:
        repository = TableRepository(db=db, entity=Day_Report)
        current_report = repository.get_by_date(date)
        return current_report
