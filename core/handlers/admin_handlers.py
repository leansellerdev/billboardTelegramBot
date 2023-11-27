from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from core.states.states import FSMStart, FSMAdminPanel

from core.database.requests.db_users import *
from core.database.requests.db_staff import *

from core.buttons.admin_buttons import admin_set_manager_kb_builder
from core.buttons.action_buttons import go_back_kb_builder
from core.buttons.action_buttons import admin_panel_kb_builder

from core.filters.admin_filters import UserIDFilter

from core.utils.staff_utils import (set_manager, is_manager, create_excel_to_send,
                                    delete_excel_file, excel_path)


admin_router: Router = Router()
today = datetime.now().strftime("%d-%m-%Y")


@admin_router.message(F.text == "Пользователи", FSMStart.start)
async def users(message: Message):

    users_list = await get_all_users()
    excel_file = FSInputFile(excel_path, filename=f"users-{today}.xlsx")

    await create_excel_to_send(users_list)

    await message.answer_document(
        document=excel_file
    )

    await delete_excel_file()


@admin_router.message(F.text == "Управление персоналом", FSMStart.start)
async def personnel_management(message: Message, state: FSMContext):

    await state.set_state(FSMAdminPanel.personal_management)

    await message.answer(
        text="Введите id пользователя",
        reply_markup=go_back_kb_builder.as_markup(resize_keyboard=True)
    )


@admin_router.message(F.text == "Менеджеры", FSMStart.start)
async def managers(message: Message):

    managers_list = await get_all_managers()
    excel_file = FSInputFile(excel_path, filename=f"managers-{today}.xlsx")

    await create_excel_to_send(managers_list)

    await message.answer_document(
        document=excel_file
    )

    await delete_excel_file()


@admin_router.message(F.text == "Назад")
async def go_back_to_main(message: Message, state: FSMContext):

    await state.set_state(FSMStart.start)

    await message.answer(
        text=f'Выберите действие:',
        reply_markup=admin_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@admin_router.message(UserIDFilter(), FSMAdminPanel.personal_management)
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


@admin_router.message(F.text, FSMAdminPanel.personal_management)
async def process_unknown_id(message: Message):

    await message.answer(
        text="Пользователь с таким ID не найден в БД"
    )


@admin_router.callback_query(F.data == "set_manager", FSMAdminPanel.set_manager)
async def set_manager_by_admin(callback: CallbackQuery, state: FSMContext):

    manager_id = await state.get_data()

    if not await is_manager(manager_id["manager_id"]):
        await set_manager(manager_id["manager_id"], True)

        await callback.message.delete()
        await callback.message.answer(
            text=f"Пользователь <b>id: {manager_id['manager_id']}</b> назначен менеджером!",
            reply_markup=admin_panel_kb_builder.as_markup(
                resize_keyboard=True
            )
        )

        await state.set_state(FSMStart.start)
    else:
        await callback.answer(
            text="Пользователь с данным ID уже назначен менеджером"
        )


@admin_router.callback_query(F.data == "unset_manager", FSMAdminPanel.set_manager)
async def unset_manager_by_admin(callback: CallbackQuery, state: FSMContext):

    manager_id = await state.get_data()

    if await is_manager(manager_id["manager_id"]):
        await set_manager(manager_id["manager_id"], False)

        await callback.message.delete()
        await callback.message.answer(
            text=f"Пользователь <b>id: {manager_id['manager_id']}</b> больше не является менеджером!",
            reply_markup=admin_panel_kb_builder.as_markup(
                resize_keyboard=True
            )
        )

        await state.set_state(FSMStart.start)
    else:
        await callback.answer(
            text="Пользователь с данным ID не является менеджером"
        )


# @admin_router.callback_query(F.data == "set_manager", FSMAdminPanel.personal_management)
# async def set_manager(callback: CallbackQuery, state: FSMContext):
#     # staff_id = int(callback.text)
#     # staffs = await set_manager_status(staff_id, True)
#     await callback.answer(text="ок")
