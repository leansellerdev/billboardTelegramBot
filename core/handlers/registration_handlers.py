from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from core.states.states import FSMRegistration, FSMStart
from core.buttons.registration_buttons import reg_end_kb_builder
from core.buttons.action_buttons import registered_kb_builder

from core.database.db import create_user

reg_router: Router = Router()


# Successful registration
@reg_router.callback_query(F.data == 'reg_end', FSMRegistration.end)
async def reg_end(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data["tg_id"]
    name = data["name"]
    surname = data["surname"]
    email = data["email"]
    phone_number = data["phone_number"]

    await create_user(user_id, name, surname, email, phone_number)

    await state.set_state(FSMStart.start)

    await callback.answer(
        text="Регистрация успешно завершена!",
        show_alert=True
    )

    await callback.message.delete()
    await callback.message.answer(
        text=f"{data}",
        reply_markup=registered_kb_builder.as_markup(
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
        reply_markup=ReplyKeyboardRemove()
    )


# 1. Enter name
@reg_router.message(F.text == "Регистрация")
async def reg_name(message: Message, state: FSMContext):

    await state.set_state(FSMRegistration.name)
    await message.answer(
        text="Напишите свое имя",
        reply_markup=ReplyKeyboardRemove()
    )


# 2. Enter surname
@reg_router.message(F.text, FSMRegistration.name)
async def reg_surname(message: Message, state: FSMContext):

    await state.update_data(
        tg_id=message.from_user.id,
        name=message.text
        )

    await state.set_state(FSMRegistration.surname)
    await message.answer(
        text="Напишите свою фамилию"
    )


# 3. Enter surname
@reg_router.message(F.text, FSMRegistration.surname)
async def reg_email(message: Message, state: FSMContext):

    await state.update_data(
        surname=message.text
    )

    await state.set_state(FSMRegistration.email)
    await message.answer(
        text="Напишите свою почту"
    )


# 4. Enter email
@reg_router.message(F.text, FSMRegistration.email)
async def reg_phone_number(message: Message, state: FSMContext):

    await state.update_data(
        email=message.text
    )

    await state.set_state(FSMRegistration.phone_number)
    await message.answer(
        text="Напишите свой номер телефона"
    )


# 5. Enter phone
@reg_router.message(F.text, FSMRegistration.phone_number)
async def reg_end(message: Message, state: FSMContext):

    await state.update_data(
        phone_number=message.text
    )

    await state.set_state(FSMRegistration.end)
    await message.answer(
        text="Завершить регистрацию?",
        reply_markup=reg_end_kb_builder.as_markup(
            resize_keyboard=True
        )
    )
