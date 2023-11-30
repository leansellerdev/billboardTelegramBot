from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from core.database.requests.staff import get_manager_users, get_manager_orders
from core.states.states import FSMManagerPanel
from core.buttons.manager_buttons import (manager_panel_statistics_kb_builder,
                                          manager_clients_actions_kb_builder,
                                          manager_billboards_actions_kb_builder)
from core.buttons.action_buttons import manager_panel_kb_builder
from core.utils.staff_utils import create_excel_to_send_manager_orders
from core.utils.users_utils import create_excel_to_send_manager_users, excel_path, delete_excel_file

manager_router: Router = Router()
today = datetime.now().strftime("%d-%m-%Y")


@manager_router.message(F.text == "Мои клиенты", FSMManagerPanel.start)
async def manager_clients(message: Message, state: FSMContext):
    await state.set_state(FSMManagerPanel.my_clients)

    await message.answer(
        text="Выберите действие:",
        reply_markup=manager_clients_actions_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@manager_router.callback_query(F.data == "clients_list", FSMManagerPanel.my_clients)
async def clients_list(callback: CallbackQuery, state: FSMContext):

    manager_id = str(callback.from_user.id)
    manager_users_list = await get_manager_users(manager_id)
    excel_file = FSInputFile(excel_path, filename=f"manager-{manager_id}-users-{today}.xlsx")

    await create_excel_to_send_manager_users(manager_users_list)

    await callback.message.answer_document(
        document=excel_file
    )
    await callback.message.delete()

    await delete_excel_file()

    await state.set_state(FSMManagerPanel.start)


@manager_router.callback_query(F.data == "orders", FSMManagerPanel.my_clients)
async def manager_orders(callback: CallbackQuery, state: FSMContext):

    order_list = await get_manager_orders(str(callback.from_user.id))

    excel_file = FSInputFile(excel_path, filename=f"manager-{str(callback.from_user.id)}-orders-{today}.xlsx")

    await create_excel_to_send_manager_orders(order_list)
    await callback.message.answer_document(
        document=excel_file
    )
    await callback.message.delete()

    await delete_excel_file()

    await state.set_state(FSMManagerPanel.start)


@manager_router.message(F.text == "Билборды", FSMManagerPanel.start)
async def billboards(message: Message, state: FSMContext):

    await state.set_state(FSMManagerPanel.billboards)
    await message.answer(
        text="Выберите действие",
        reply_markup=manager_billboards_actions_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@manager_router.message(F.text == "Назад", FSMManagerPanel.billboards)
async def go_back_to_manager_menu(message: Message, state: FSMContext):

    await state.set_state(FSMManagerPanel.start)

    await message.answer(
        text="Выберите действие:",
        reply_markup=manager_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@manager_router.message(F.text == "Статистика", FSMManagerPanel.start)
async def statistics(message: Message, state: FSMContext):

    await state.set_state(FSMManagerPanel.statistics)

    await message.answer(
        text="Вы на панели статистики! \nВыберите действие:",
        reply_markup=manager_panel_statistics_kb_builder.as_markup(resize_keyboard=True)
    )


@manager_router.message(F.text == "Назад", FSMManagerPanel.statistics)
async def go_back_to_manager_menu(message: Message, state: FSMContext):

    await state.set_state(FSMManagerPanel.start)

    await message.answer(
        text="Выберите действие:",
        reply_markup=manager_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )
