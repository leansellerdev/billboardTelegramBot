from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from core.states.states import FSMStart, FSMChangeData
from core.buttons.action_buttons import cancel_kb_builder, registered_kb_builder

from core.database.users.db_users import change_user_phone, change_user_email

from core.utils.utils import user_registered


command_router: Router = Router()


@command_router.message(Command(commands=['change_phone_number']), FSMStart.start)
async def change_phone_number(message: Message, state: FSMContext):

    if not await user_registered(message.from_user.id):

        await message.answer(
            text="Менять номер телефона могут только зарегистрированные пользователи\n"
                 "Для регистрации нажмите сюда - /registration"
        )
    else:

        await state.set_state(FSMChangeData.change_phone)
        await message.answer(
            text="Введите новый номер телефона:",
            reply_markup=cancel_kb_builder.as_markup(
                resize_keyboard=True
            )
        )


@command_router.message(F.text, FSMChangeData.change_phone)
async def complete_change_phone_number(message: Message, state: FSMContext):

    await change_user_phone(message.from_user.id, message.text)
    await message.answer(
        text=f"Ваш номер успешно изменен на {message.text}",
        reply_markup=registered_kb_builder.as_markup(
            resize_keyboard=True
        )
    )

    await state.set_state(FSMStart.start)


@command_router.message(Command(commands=['change_email_address']), FSMStart.start)
async def change_email_address(message: Message, state: FSMContext):

    if not await user_registered(message.from_user.id):

        await message.answer(
            text="Менять адрес электронной почты могут только зарегистрированные пользователи\n"
                 "Для регистрации нажмите сюда - /registration"
        )
    else:

        await state.set_state(FSMChangeData.change_email)
        await message.answer(
            text="Введите новый адрес почты:",
            reply_markup=cancel_kb_builder.as_markup(
                resize_keyboard=True
            )
        )


@command_router.message(F.text, FSMChangeData.change_email)
async def complete_change_email_address(message: Message, state: FSMContext):

    await change_user_email(message.from_user.id, message.text)
    await message.answer(
        text=f"Ваш адрес электронной почты успешно изменен на {message.text}",
        reply_markup=registered_kb_builder.as_markup(
            resize_keyboard=True
        )
    )

    await state.set_state(FSMStart.start)
