from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.states.states import FSMStart

users_router: Router = Router()


@users_router.message(F.text == "Мои заказы", FSMStart.start)
async def self_orders(message: Message, state: FSMContext):

    # await state.set_state(FSMStart.self_orders)

    await message.answer(
        text="Coming Soon..."
    )


@users_router.message(F.text == "Биллборды", FSMStart.start)
async def billboards(message: Message, state: FSMContext):

    # await state.set_state(FSMStart.billboards)

    await message.answer(
        text="Coming Soon..."
    )


@users_router.message(F.text == "О нас", FSMStart.start)
async def about_us(message: Message, state: FSMContext):

    # await state.set_state(FSMStart.about)

    await message.answer(
        text="Coming Soon..."
    )
