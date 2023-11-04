from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import text

router = Router()


@router.message(Command("help"))
async def help_handler(msg: Message):
    await msg.answer(text=text.help.format())


@router.message(Command("security"))
async def security_handler(msg: Message):
    await msg.answer(text=text.security.format())


@router.message(Command("information"))
async def information_handler(msg: Message):
    await msg.answer(text=text.information.format())
