from aiogram import Bot
from aiogram.types import BotCommand,BotCommandScopeDefault

async def set_commnads(bot:Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начать работу с ботом или получить базовую информацию'),
        BotCommand(
            command='report',
            description='Занести отчет или посмотреть конкретный прием пищи'
        ),
        BotCommand(
            command='show',
            description='Показать информацию за выбранный день'
        ),
        BotCommand(
            command='pdf',
            description='Сформировать отчет за выбранный месяц'
        ),
        BotCommand(
            command='help',
            description='Получть весь список команд'
        ),
        BotCommand(
            command='security',
            description='Получить информацию почему бот безопасный для использования'
        )
    ]

    await bot.set_my_commands(commands,BotCommandScopeDefault())