import calendar
import os
from datetime import date
from datetime import datetime

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command

from GenericRepository import TableRepository
from database.database import engine as database
from database.database import Day_Report
from sqlalchemy.orm import Session
from pdf_former import start

import keyboard
import text

router = Router()


class Month(StatesGroup):
    month = State()


@router.message(Command("pdf"))
async def get_pdf(msg: Message, state=FSMContext):
    await state.set_state(Month.month)
    await msg.answer(text=text.choose_month.format(year=datetime.now().year),
                     reply_markup=await keyboard.get_month_keyboard())


@router.callback_query(Month.month)
async def choose_report_day(msg: CallbackQuery, bot: Bot, state=FSMContext):
    data = msg.data
    await state.update_data(month=data)
    data = await state.get_data()
    await state.clear()
    lines = await get_report_by_year_and_month(datetime.now().year, int(msg.data), msg.from_user.id)
    if lines is not None:
        await msg.message.answer(
            text=f"Отчет за {calendar.month_name[int(msg.data)]} {datetime.now().year} файл уже формируется.")
        await start(lines,
                    f"{msg.from_user.full_name}_{msg.from_user.id}_{calendar.month_name[int(msg.data)]}_{datetime.now().year}")
        doc = FSInputFile(
            path=f"{msg.from_user.full_name}_{msg.from_user.id}_{calendar.month_name[int(msg.data)]}_{datetime.now().year}.pdf")
        await bot.send_document(msg.message.chat.id, document=doc)
        os.remove(
            f"{msg.from_user.full_name}_{msg.from_user.id}_{calendar.month_name[int(msg.data)]}_{datetime.now().year}.pdf")

    else:
        await msg.message.answer(text="В выбранный вами месяц нет данных")


async def get_report_by_year_and_month(year: int, month: int, id: int):
    with Session(autoflush=False, bind=database.engine) as db:
        repository = TableRepository(db=db, entity=Day_Report)
        current_report = repository.all_reports_by_year_and_month(year, month, id)
        return current_report
