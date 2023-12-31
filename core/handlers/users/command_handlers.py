from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from core.states.states import FSMStart, FSMChangeData
from core.buttons.action_buttons import cancel_kb_builder, user_panel_kb_builder

from core.database.requests.users import change_user_phone, change_user_email

from core.utils.users_utils import user_registered
from core.filters.registration_filters import EmailFilter, PhoneFilter


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


@command_router.message(PhoneFilter(), FSMChangeData.change_phone)
async def complete_change_phone_number(message: Message, state: FSMContext):

    await change_user_phone(message.from_user.id, message.text)
    await message.answer(
        text=f"Ваш номер успешно изменен на {message.text}",
        reply_markup=user_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )

    await state.set_state(FSMStart.start)


@command_router.message(FSMChangeData.change_phone)
async def process_incorrect_phone(message: Message):

    await message.answer(
        text="Некорректный номер телефона\n"
             "Введи номер Вашего телефона в виде +1 234 567 8901"
    )


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


@command_router.message(EmailFilter(), FSMChangeData.change_email)
async def complete_change_email_address(message: Message, state: FSMContext):

    await change_user_email(message.from_user.id, message.text)
    await message.answer(
        text=f"Ваш адрес электронной почты успешно изменен на {message.text}",
        reply_markup=user_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )

    await state.set_state(FSMStart.start)


@command_router.message(FSMChangeData.change_email)
async def process_incorrect_email(message: Message):

    await message.answer(
        text="Некорректный адрес почты!\n"
             "Введите адрес Вашей почты в виде example@example.com"
    )
