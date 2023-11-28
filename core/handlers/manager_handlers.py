from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from core.database.requests.db_staff import get_manager_users, get_manager_orders
from core.database.requests.db_billboards import create_billboard
from core.states.states import FSMStart, FSMManagerPanel, FSMCreateBillboard
from core.buttons.action_buttons import (manager_panel_statistics_kb_builder)
from core.utils.staff_utils import create_excel_to_send_manager_orders
from core.utils.users_utils import create_excel_to_send_manager_users, excel_path, delete_excel_file

manager_router: Router = Router()
today = datetime.now().strftime("%d-%m-%Y")


@manager_router.message(F.text == "Мои пользователи", FSMStart.start)
async def manager_users(message: Message, state: FSMContext):
    manager_id = str(message.from_user.id)
    manager_users_list = await get_manager_users(manager_id)
    excel_file = FSInputFile(excel_path, filename=f"manager-{manager_id}-users-{today}.xlsx")

    await create_excel_to_send_manager_users(manager_users_list)

    await message.answer_document(
        document=excel_file
    )

    await delete_excel_file()


@manager_router.message(F.text == "Статистика", FSMStart.start)
async def statistics(message: Message, state: FSMContext):

    await state.set_state(FSMManagerPanel.statistics)

    await message.answer(
        text="Вы на панели статистики! \nВыберите действие:",
        reply_markup=manager_panel_statistics_kb_builder.as_markup(resize_keyboard=True)
    )


@manager_router.message(F.text == "Назначенные заказы", FSMStart.start)
async def manager_orders(message: Message):
    order_list = await get_manager_orders(str(message.from_user.id))

    excel_file = FSInputFile(excel_path, filename=f"manager-{str(message.from_user.id)}-orders-{today}.xlsx")

    await create_excel_to_send_manager_orders(order_list)

    await message.answer_document(
        document=excel_file
    )

    await delete_excel_file()

