from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext

from core.states.states import FSMStart, FSMAdminPanel
from core.buttons.action_buttons import (not_registered_kb_builder,
                                         registered_kb_builder, admin_panel_kb_builder)

from core.utils.users_utils import user_registered
from core.utils.staff_utils import *
from core.database.db_users import *
from core.database.requests.db_staff import *
from core.buttons.admin_buttons import *

router: Router = Router()
# user_registered = False


@router.message(CommandStart())
@router.message(Command(commands=["cancel"]))
@router.message(F.text == "Отмена")
async def start(message: Message, state: FSMContext):
    username = message.from_user.first_name
    await state.set_state(FSMStart.start)

    if await is_admin(message.from_user.id):
        await message.answer(
            text=f'Здравствуйте, {username}!\nВыберите действие:',
            reply_markup=admin_panel_kb_builder.as_markup(
                resize_keyboard=True
            )
        )
    elif not await user_registered(message.from_user.id):
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


@router.message(F.text == "Пользователи", FSMStart.start)
async def users(message: Message, state: FSMContext):

    await state.set_state(FSMAdminPanel.get_users)

    users = await get_all_users()

    await message.answer(
        text=f'{users}'
    )


@router.message(F.text == "Управление персоналом", FSMStart.start)
async def personnel_management(message: Message, state: FSMContext):

    await state.set_state(FSMAdminPanel.personal_management)

    await message.answer(
        text="Введите id пользователя",
        #reply_markup=admin_set_manager_kb_builder.as_markup(resize_keyboard=True)
    )


@router.message(F.text, FSMAdminPanel.personal_management)
async def get_user_id(message: Message, state: FSMContext):

    await state.set_state(FSMAdminPanel.set_manager)

    await state.update_data(
        manager_id=message.text
    )

    await message.answer(
        text="Выберите действие",
        reply_markup=admin_set_manager_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@router.callback_query(F.data == "set_manager", FSMAdminPanel.set_manager)
async def set_manager_by_admin(callback: CallbackQuery, state: FSMContext):

    manager_id = await state.get_data()

    await set_manager_status(manager_id["manager_id"], True)

    await callback.message.delete()
    await callback.answer(
        text=f"Пользователь id: {manager_id['manager_id']} назначен менеджером!"
    )


@router.callback_query(F.data == "set_manager", FSMAdminPanel.personal_management)
async def set_manager(callback: CallbackQuery, state: FSMContext):
    # staff_id = int(callback.text)
    # staffs = await set_manager_status(staff_id, True)
    await callback.answer(text="ок")


@router.message(F.text == "Менеджеры", FSMStart.start)
async def managers(message: Message, state: FSMContext):

    #await state.set_state(FSMAdminPanel.get_managers)

    staffs = await get_all_managers()

    await message.answer(
        text=f'{staffs}'
    )