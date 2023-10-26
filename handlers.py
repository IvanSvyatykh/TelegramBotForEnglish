from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

import keyboard
import text

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.start.format(name=msg.from_user.full_name), reply_markup=keyboard.get_reply_keyboard())


@router.message(F.contact)
async def get_contact(msg: Message):
    await msg.answer(f"Спасибо, {msg.from_user.full_name}.\n"
                         f"Ваш номер {msg.contact.phone_number} был получен")