import calendar
import json
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

import keyboard
import text

router = Router()


class PersonReport(StatesGroup):
    month = State()
    day = State()
    meal = State()
    report_id = State()
    breakfast = State()
    lunch = State()
    dinner = State()
    see_report = State()


@router.message(Command("report"))
async def choose_report_month(msg: Message, state=FSMContext):
    await state.set_state(PersonReport.month)
    await msg.answer(text=text.choose_month.format(year=datetime.now().year),
                     reply_markup=await keyboard.get_month_keyboard())


@router.message(Command("cancel"))
async def cancel_month(msg: Message, state=FSMContext):
    await state.clear()
    await msg.answer(text="Операция остановлена")


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
    if msg.data == "Сохранить":

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
    else:
        await state.set_state(PersonReport.see_report)
        await msg.message.answer(
            text="Выберите вариант работы с отчетом.Внимание, если вы выберите существующий прием пищи в режиме редактирования, данные перезапишутся",
            reply_markup=await keyboard.get_variants())


@router.message(PersonReport.see_report)
async def see_or_add(msg: Message, state=FSMContext):
    if msg.text == "Добавить":
        await state.set_state(ReportState.bread_units)
        await msg.answer(
            text="Введите количество хлебных единиц за прием, если вы не хотите вводить их введите символ - .")

    if ((msg.text == "Просмотреть") and (await get_current_meal(await state.get_data()) is None)):
        await state.set_state(ReportState.bread_units)
        await msg.answer(
            text="Выбранный прием пищи не заполнен,сначал заполните его.Введите количество хлебных единиц за прием, если вы не хотите вводить их введите символ - .")
    elif msg.text == "Просмотреть":
        data = await state.get_data()
        meal = await get_current_meal(data)
        meal = meal.replace("\"", "")
        meal = meal.replace("{", "")
        meal = meal.replace("}", "")
        meal = meal.split(",")
        await state.clear()
        await msg.answer(text=text.report.format(meal=data["meal"], date=date(datetime.now().year, int(data["month"]),
                                                                              int(data["day"])).strftime("%d-%m-%Y"),
                                                 bread_units=meal[0],
                                                 short_insulin=meal[1].replace(" ", "", 1),
                                                 long_insulin=meal[2].replace(" ", "", 1),
                                                 sugar_before=meal[3].replace(" ", "", 1),
                                                 sugar_after=meal[4].replace(" ", "", 1),
                                                 report=meal[5].replace(" ", "", 1)))


async def get_current_meal(data):
    if (data["meal"] == "Завтрак"):
        return data["breakfast"]
    elif (data["meal"] == "Обед"):
        return data["lunch"]
    elif (data["meal"] == "Ужин"):
        return data["dinner"]


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


class ReportState(StatesGroup):
    bread_units = State()
    short_insulin = State()
    long_insulin = State()
    sugar_before = State()
    sugar_after = State()
    report = State()
    finish = State()


@router.message(ReportState.bread_units)
async def ask_short_insulin(msg: Message, state=FSMContext):
    if msg.text.isdecimal() or msg.text == "-":
        await state.update_data(bread_units=msg.text)
        await state.set_state(ReportState.short_insulin)
        await msg.answer(
            text="Отлично! Добавьте значение короткого инсулина, если вы не хотите вводить их введите символ - ")
    else:
        await msg.answer(text="Введеное значение не может быть числом, введите хлебные еденицы заново")


@router.message(ReportState.short_insulin)
async def ask_long_insulin(msg: Message, state=FSMContext):
    if msg.text.isdecimal() or msg.text == "-":
        await state.update_data(short_insulin=msg.text)
        await state.set_state(ReportState.long_insulin)
        await msg.answer(
            text="Отлично! Добавьте значение длинного инсулина  еды, если вы не хотите вводить их введите символ - ")
    else:
        await msg.answer(text="Введеное значение не может быть числом, введите короткий инсулин заново")


@router.message(ReportState.long_insulin)
async def ask_sugar_before(msg: Message, state=FSMContext):
    if msg.text.isdecimal() or msg.text == "-":
        await state.update_data(long_insulin=msg.text)
        await state.set_state(ReportState.sugar_before)
        await msg.answer(
            text="Отлично! Добавьте значение сахара до еды, если вы не хотите вводить их введите символ - ")
    else:
        await msg.answer(text="Введеное значение не может быть числом, введите длинный инсулин  заново")


@router.message(ReportState.sugar_before)
async def ask_sugar_after(msg: Message, state=FSMContext):
    if msg.text.isdecimal() or msg.text == "-":
        await state.update_data(sugar_before=msg.text)
        await state.set_state(ReportState.sugar_after)
        await msg.answer(
            text="Отлично! Добавьте значение сахара после еды, если вы не хотите вводить их введите символ - ")
    else:
        await msg.answer(text="Введеное значение не может быть числом, введите сахар до еды заново")


@router.message(ReportState.sugar_after)
async def ask_health(msg: Message, state=FSMContext):
    if msg.text.isdecimal() or msg.text == "-":
        await state.update_data(sugar_after=msg.text)
        await state.set_state(ReportState.report)
        await msg.answer(
            text="Отлично! Добавьте описание своего самочувствия")
    else:
        await msg.answer(text="Введеное значение не может быть числом, введите сахар после еды заново")


@router.message(ReportState.report)
async def final(msg: Message, state=FSMContext):
    await state.update_data(report=msg.text)
    await state.set_state(ReportState.finish)
    await msg.answer(
        text="Отлично! Все готово.", reply_markup=await keyboard.get_confirmation())


@router.message(ReportState.finish)
async def final(msg: Message, state=FSMContext):
    if msg.text == "Отмена":
        await msg.answer(text="Оформление остановлено!")
        await state.clear()
        return

    data = await state.get_data()
    await update_state(data, state)
    res = await form_dic(data)

    await state.clear()

    current_report = await get_report_by_date_and_id(date(datetime.now().year, int(data["month"]), int(data["day"])),
                                                     msg.from_user.id)
    if current_report is None:
        if data["meal"] == "Завтрак":
            data["breakfast"] = json.dumps(res, ensure_ascii=False)
            data["lunch"] = sqlalchemy.sql.null()
            data["dinner"] = sqlalchemy.sql.null()
        if data["meal"] == "Обед":
            data["lunch"] = json.dumps(res, ensure_ascii=False)
            data["breakfast"] = sqlalchemy.sql.null()
            data["dinner"] = sqlalchemy.sql.null()
        if data["meal"] == "Ужин":
            data["dinner"] = json.dumps(res, ensure_ascii=False)
            data["breakfast"] = sqlalchemy.sql.null()
            data["lunch"] = sqlalchemy.sql.null()

        report = Day_Report(person_id=msg.from_user.id,
                            breakfast=data["breakfast"],
                            lunch=data["lunch"],
                            dinner=data["dinner"],
                            date=date(datetime.now().year, int(data["month"]), int(data["day"])))

        await save_report(report, msg)
    else:
        if data["meal"] == "Завтрак":
            data["breakfast"] = json.dumps(res, ensure_ascii=False)
        if data["meal"] == "Обед":
            data["lunch"] = json.dumps(res, ensure_ascii=False)
        if data["meal"] == "Ужин":
            data["dinner"] = json.dumps(res, ensure_ascii=False)
        current_report = await update_data(current_report, data)
        await save_report(current_report, msg)


async def form_dic(data, state=FSMContext) -> dict:
    report = {}
    report['Хлебные еденицы'] = data["bread_units"]
    report['Короткий инсулин'] = data["short_insulin"]
    report['Длинный инсулин'] = data["long_insulin"]
    report['Сахар до'] = data["sugar_before"]
    report['Сахар после'] = data["sugar_after"]
    report['Самочувствие'] = data["report"]
    return report
