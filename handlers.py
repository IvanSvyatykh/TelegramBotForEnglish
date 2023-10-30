from aiogram import types, F, Router
from aiogram.types import Message, InlineQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from GenericRepository import TableRepository
from sqlalchemy.orm import Session
from typing import Any, Dict

import database
import keyboard
import text

router = Router()


class CurrentPerson(StatesGroup):
    id = State()
    name = State()
    diabetes_type = State()


@router.message(CommandStart())
async def start_handler(msg: Message, state=FSMContext) -> None:
    with Session(autoflush=False, bind=database.engine) as db:
        repository = TableRepository(db=db, entity=database.Person)

    if (repository.get_by_id(id=msg.from_user.id) == None):
        await state.set_state(CurrentPerson.diabetes_type)
        await msg.answer(
            text=text.start_registration.format(name=msg.from_user.full_name),
            reply_markup=keyboard.get_diabet_type_keyboard(),
        )


@router.message(CurrentPerson.diabetes_type)
async def set_diabetes_type_handler(msg: Message, state=FSMContext) -> None:
    data = await state.update_data(diabetes_type=msg.text, id=msg.from_user.id, name=msg.from_user.full_name)
    await state.clear()
    await show_summary(msg, data)


async def show_summary(msg: Message, data: Dict[str, Any]):
    with Session(autoflush=False, bind=database.engine) as db:
        repository = TableRepository(db=db, entity=database.Person)
        user_to_db = database.Person()
        user_to_db.id = data["id"]
        user_to_db.name = data["name"]
        user_to_db.type_of_diabet = data["diabetes_type"]
        repository.add_user(user_to_db)
    await msg.answer(text=text.registration.format(name=data["name"], id=data["id"], diabetes_type=data["diabetes_type"]))

