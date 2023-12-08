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

import keyboard
import text

router = Router()


class ChooseReport(StatesGroup):
    month = State()
    day = State()
    breakfast = State()
    lunch = State()
    dinner = State()


@router.message(Command("show"))
async def choose_report_month(msg: Message, state=FSMContext):
    await state.set_state(ChooseReport.month)
    await msg.answer(text=text.choose_month.format(year=datetime.now().year),
                     reply_markup=await keyboard.get_month_keyboard())


@router.callback_query(ChooseReport.month)
async def choose_report_day(msg: CallbackQuery, state=FSMContext):
    data = msg.data
    await state.update_data(month=data)
    await state.set_state(ChooseReport.day)
    await msg.message.answer(
        text=text.choose_day.format(year=datetime.now().year, month=calendar.month_name[int(data)]),
        reply_markup=await keyboard.get_days_keyboard(data))


@router.callback_query(ChooseReport.day)
async def choose_part_of_day(msg: CallbackQuery, state=FSMContext):
    await state.update_data(day=msg.data)
    data = await state.get_data()

    current_report = await get_report_by_date_and_id(date(datetime.now().year, int(data["month"]), int(data["day"])),
                                                     msg.from_user.id)
    if current_report is None:
        await msg.message.answer(text="В выбранную дату ничего нет.\n"
                                      "Воспользуйтесь командой /report для заполнения данных.")
    else:

        await set_state(current_report, state)
        data = await state.get_data()

        breakfast = []
        lunch = []
        dinner = []
        if data["breakfast"] is not None:
            breakfast = await get_report_arr("Завтрак", data)
            breakfast = text.show_report.format(meal="Завтрак", bread_units=breakfast[0],
                                                short_insulin=breakfast[1].replace(" ", "", 1),
                                                long_insulin=breakfast[2].replace(" ", "", 1),
                                                sugar_before=breakfast[3].replace(" ", "", 1),
                                                sugar_after=breakfast[4].replace(" ", "", 1),
                                                report=breakfast[5].replace(" ", "", 1))
        else:
            breakfast = text.show_empty_report.format(meal="Завтрак", report="Этот прием пищи пуст.")

        if data["lunch"] is not None:
            lunch = await get_report_arr("Обед", data)
            lunch = text.show_report.format(meal="Обед", bread_units=lunch[0],
                                            short_insulin=lunch[1].replace(" ", "", 1),
                                            long_insulin=lunch[2].replace(" ", "", 1),
                                            sugar_before=lunch[3].replace(" ", "", 1),
                                            sugar_after=lunch[4].replace(" ", "", 1),
                                            report=lunch[5].replace(" ", "", 1))
        else:
            lunch = text.show_empty_report.format(meal="Обед", report="Этот прием пищи пуст.")

        if data["dinner"] is not None:
            dinner = await get_report_arr("Ужин", data)
            dinner = text.show_report.format(meal="Ужин", bread_units=dinner[0],
                                             short_insulin=dinner[1].replace(" ", "", 1),
                                             long_insulin=dinner[2].replace(" ", "", 1),
                                             sugar_before=dinner[3].replace(" ", "", 1),
                                             sugar_after=dinner[4].replace(" ", "", 1),
                                             report=dinner[5].replace(" ", "", 1))
        else:
            dinner = text.show_empty_report.format(meal="Ужин", report="Этот прием пищи пуст.")

        await msg.message.answer(
            text="Дата: " + date(datetime.now().year, int(data["month"]), int(data["day"])).strftime(
                "%d-%m-%Y") + "\n" + breakfast + "\n" + lunch + "\n" + dinner)

        await state.clear()


async def get_report_by_date_and_id(date: datetime, id: int):
    with Session(autoflush=False, bind=database.engine) as db:
        repository = TableRepository(db=db, entity=Day_Report)
        current_report = repository.get_by_date_and_id(date, id)
        return current_report


async def set_state(current_report: Day_Report, state=FSMContext):
    await state.set_state(ChooseReport.breakfast)
    await state.update_data(breakfast=current_report.breakfast)
    await state.set_state(ChooseReport.lunch)
    await state.update_data(lunch=current_report.lunch)
    await state.set_state(ChooseReport.dinner)
    await state.update_data(dinner=current_report.dinner)


@router.message(Command("back"), ChooseReport.day)
async def back_to_month(msg: Message, state=FSMContext):
    await state.set_state(ChooseReport.month)
    await msg.answer(text=text.choose_month.format(year=datetime.now().year),
                     reply_markup=await keyboard.get_month_keyboard())


@router.message(Command("cancel"))
async def cancel_month(msg: Message, state=FSMContext):
    await state.clear()
    await msg.answer(text="Операция остановлена")


async def get_report_arr(meal: str, data):
    if ("Завтрак" == meal):
        return data["breakfast"].replace("\"", "").replace("{", "").replace("}", "").split(",")

    if ("Обед" == meal):
        return data["lunch"].replace("\"", "").replace("{", "").replace("}", "").split(",")

    if ("Ужин" == meal):
        return data["dinner"].replace("\"", "").replace("{", "").replace("}", "").split(",")
