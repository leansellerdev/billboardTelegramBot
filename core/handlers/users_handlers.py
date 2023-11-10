from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from core.buttons.action_buttons import (not_registered_kb_builder,
                                         registered_kb_builder)

router: Router = Router()
user_registered = False


@router.message(Command(commands=['start']))
async def start(message: Message):
    username = message.from_user.first_name

    if not user_registered:
        await message.answer(
            text=f'Ваш username: {username}',
            reply_markup=not_registered_kb_builder.as_markup(
                resize_keyboard=True
            )
        )
    else:
        await message.answer(
            text=f'Ваш username: {username}',
            reply_markup=registered_kb_builder.as_markup(
                resize_keyboard=True
            )
        )
