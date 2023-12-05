from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from GenericRepository import TableRepository
from sqlalchemy.orm import Session
from typing import Any, Dict

from database.database import engine as database
from database.database import Person
import keyboard
import text
from handlers.help_handler import help_handler

router = Router()


class CurrentPerson(StatesGroup):
    id = State()
    name = State()
    diabetes_type = State()


@router.message(CommandStart())
async def start_handler(msg: Message, state=FSMContext) -> None:
    with Session(autoflush=False, bind=database.engine) as db:
        repository = TableRepository(db=db, entity=Person)
        current_user = repository.get_by_id(id=msg.from_user.id)
    if current_user is None:
        await state.set_state(CurrentPerson.diabetes_type)
        await msg.answer(
            text=text.start_registration.format(name=msg.from_user.full_name),
            reply_markup=await keyboard.get_diabetes_type_keyboard(),
        )
    else:
        await state.clear()
        await msg.answer(text=text.greetings.format(name=current_user.name, id=current_user.id,
                                                    diabetes_type=current_user.diabetes_type))
        await help_handler(msg)


@router.message(CurrentPerson.diabetes_type)
async def set_diabetes_type_handler(msg: Message, state=FSMContext) -> None:
    data = await state.update_data(diabetes_type=msg.text, id=msg.from_user.id, name=msg.from_user.full_name)
    await state.clear()
    await show_summary(msg, data)


async def save_user_to_db(data: Dict[str, Any]):
    with Session(autoflush=False, bind=database.engine) as db:
        repository = TableRepository(db=db, entity=Person)
        user_to_db = Person(id=data["id"], name=data["name"], diabetes_type=data["diabetes_type"])
        repository.add(user_to_db)


async def show_summary(msg: Message, data: Dict[str, Any]):
    await save_user_to_db(data)
    await msg.answer(
        text=text.registration.format(name=data["name"], id=data["id"], diabetes_type=data["diabetes_type"]))
    await help_handler(msg)
