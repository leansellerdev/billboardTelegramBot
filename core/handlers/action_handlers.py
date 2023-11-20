from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext

from core.states.states import FSMStart
from core.buttons.action_buttons import (not_registered_kb_builder,
                                         registered_kb_builder)

from core.utils.users_utils import user_registered

router: Router = Router()
# user_registered = False


@router.message(CommandStart())
@router.message(Command(commands=["cancel"]))
@router.message(F.text == "Отмена")
async def start(message: Message, state: FSMContext):
    username = message.from_user.first_name
    await state.set_state(FSMStart.start)

    if not await user_registered(message.from_user.id):
        await message.answer(
            text=f'Здравствуйте, {username}!\n\n'
                 f'Для доступа к полному функционалу Вам необходимо зарегистрироваться - /registration',
            reply_markup=not_registered_kb_builder.as_markup(
                resize_keyboard=True
            )
        )
    else:
        await message.answer(
            text=f'Здравствуйте, {username}!\nВыберите действие:',
            reply_markup=registered_kb_builder.as_markup(
                resize_keyboard=True
            )
        )


@router.message(F.text == "Мои заказы", FSMStart.start)
async def self_orders(message: Message, state: FSMContext):

    # await state.set_state(FSMStart.self_orders)

    await message.answer(
        text="Coming Soon..."
    )


@router.message(F.text == "Биллборды", FSMStart.start)
async def billboards(message: Message, state: FSMContext):

    # await state.set_state(FSMStart.billboards)

    await message.answer(
        text="Coming Soon..."
    )


@router.message(F.text == "О нас", FSMStart.start)
async def about_us(message: Message, state: FSMContext):

    # await state.set_state(FSMStart.about)

    await message.answer(
        text="Coming Soon..."
    )
