import asyncio
import logging
import config

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start_handler, help_handler, add_report_handler, get_report_handler, form_pdf_report
from bot_commands import set_commnads


async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await set_commnads(bot)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_handler.router)
    dp.include_router(help_handler.router)
    dp.include_router(add_report_handler.router)
    dp.include_router(get_report_handler.router)
    dp.include_router(form_pdf_report.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
