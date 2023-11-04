from aiogram import Router
from aiogram.types import Message , CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from datetime import datetime

import keyboard
import text

router = Router()


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
    await state.update_data(month=msg.data)
    await state.set_state(PersonReport.day)
    await msg.answer(text=text.choose_day.format(year=datetime.now().year, month=PersonReport.month),
                     reply_markup=keyboard.get_days_keyboard(PersonReport.month))
