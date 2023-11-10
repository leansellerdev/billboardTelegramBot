from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

router: Router = Router()


@router.message(Command(commands=['start']))
async def start(message: Message):
    username = message.from_user.first_name

    await message.answer(
        text=f'Ваш username: {username}',
    )
