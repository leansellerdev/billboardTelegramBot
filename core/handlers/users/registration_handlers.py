from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from core.database.requests.staff import get_manager_with_min_users
from core.states.states import FSMRegistration, FSMStart
from core.buttons.registration_buttons import reg_end_kb_builder
from core.buttons.action_buttons import user_panel_kb_builder, go_back_kb_builder, not_registered_kb_builder

from core.database.requests.users import create_user
from core.utils.users_utils import user_registered, get_user_info
from core.filters.registration_filters import EmailFilter, PhoneFilter

reg_router: Router = Router()


# Successful registration
@reg_router.callback_query(F.data == 'reg_end', FSMRegistration.end)
async def reg_end(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await create_user(user=data)

    await state.set_state(FSMStart.start)

    await callback.answer(
        text="Регистрация успешно завершена!",
        show_alert=True
    )

    user_info = await get_user_info(callback.from_user.id)

    await callback.message.delete()
    await callback.message.answer(
        text=user_info,
        reply_markup=user_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


# Change user data
@reg_router.callback_query(F.data == 'change_data', FSMRegistration.end)
async def change_reg_date(callback: CallbackQuery, state: FSMContext):

    await state.set_state(FSMRegistration.name)

    await callback.message.delete()
    await callback.message.answer(
        text="Напишите свое имя",
        reply_markup=go_back_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


# 1. Enter name
@reg_router.message(Command(commands=["registration"]))
@reg_router.message(F.text == "Регистрация")
async def reg_name(message: Message, state: FSMContext):

    if await user_registered(message.from_user.id):
        await message.answer(
            text="Вы уже зарегистрированы!"
        )
    else:
        await state.set_state(FSMRegistration.name)
        await message.answer(
            text="Напишите свое имя\n\n"
                 "Чтобы отменить регистрацию напишите - /cancel",
            reply_markup=go_back_kb_builder.as_markup(
                resize_keyboard=True
            )
        )


# 2. Enter surname
@reg_router.message(F.text, FSMRegistration.name)
async def reg_surname(message: Message, state: FSMContext):

    await state.update_data(
        tg_id=message.from_user.id,
        name=message.text
        )

    if message.text == "Назад":
        await state.set_state(FSMStart.start)

        await message.answer(
            text="Регистрация отменена",
            reply_markup=not_registered_kb_builder.as_markup(
                resize_keyboard=True
            )
        )
    else:
        await state.set_state(FSMRegistration.surname)
        await message.answer(
            text="Напишите свою фамилию",
            reply_markup=(go_back_kb_builder.as_markup(
                resize_keyboard=True
            ))
        )


@reg_router.message(F.text == "Назад", FSMRegistration.surname)
async def back_to_name(message: Message, state: FSMContext):

    await state.set_state(FSMRegistration.name)

    await message.answer(
        text="Напишите свое имя"
    )


# 3. Enter email
@reg_router.message(F.text, FSMRegistration.surname)
async def reg_email(message: Message, state: FSMContext):

    await state.update_data(
        surname=message.text
    )

    await state.set_state(FSMRegistration.email)
    await message.answer(
        text="Напишите свою почту"
    )


@reg_router.message(F.text == "Назад", FSMRegistration.email)
async def back_to_surname(message: Message, state: FSMContext):

    await state.set_state(FSMRegistration.surname)

    await message.answer(
        text="Напишите свою фамилию"
    )


# 4. Enter phone
@reg_router.message(EmailFilter(), FSMRegistration.email)
async def reg_phone_number(message: Message, state: FSMContext):

    await state.update_data(
        email=message.text
    )

    await state.set_state(FSMRegistration.phone_number)
    await message.answer(
        text="Напишите свой номер телефона"
    )


@reg_router.message(F.text == "Назад", FSMRegistration.phone_number)
async def back_to_email(message: Message, state: FSMContext):

    await state.set_state(FSMRegistration.email)

    await message.answer(
        text="Напишите свою почту"
    )


@reg_router.message(FSMRegistration.email)
async def process_incorrect_email(message: Message):

    await message.answer(
        text="Некорректный адрес почты!\n"
             "Введите адрес Вашей почты в виде example@example.com"
    )


# 5. Reg last step
@reg_router.message(PhoneFilter(), FSMRegistration.phone_number)
async def reg_end(message: Message, state: FSMContext):

    manager_id = await get_manager_with_min_users()

    await state.update_data(
        phone_number=message.text,
        manager_id=manager_id
    )

    await state.set_state(FSMRegistration.end)
    await message.answer(
        text="Завершить регистрацию?",
        reply_markup=reg_end_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@reg_router.message(F.text == "Назад", FSMRegistration.end)
async def back_to_phone_number(message: Message, state: FSMContext):

    await state.set_state(FSMRegistration.phone_number)

    await message.answer(
        text="Напишите свой номер телефона"
    )


@reg_router.message(FSMRegistration.phone_number)
async def process_incorrect_phone(message: Message):

    await message.answer(
        text="Некорректный номер телефона\n"
             "Введи номер Вашего телефона в виде +1 234 567 8901"
    )
