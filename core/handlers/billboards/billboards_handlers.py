from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from core.database.requests.billboards import change_price

from core.states.states import FSMManagerPanel, FSMBillboards
from core.utils.billboard_utils import get_billboard_info_by_name

from core.buttons.billboards_buttons import change_billboard_data_kb_builder
from core.buttons.action_buttons import manager_panel_kb_builder
from core.buttons.manager_buttons import manager_billboards_actions_kb_builder

from core.filters.billboard_filters import BillboardExistsFilter

billboards_router: Router = Router()


@billboards_router.message(F.text == "Изменить билборд", FSMManagerPanel.billboards)
async def get_billboard_name(message: Message, state: FSMContext):

    await state.set_state(FSMBillboards.billboard_name)

    await message.answer(
        text="Введите название билборда",
        reply_markup=ReplyKeyboardRemove()
    )


@billboards_router.message(BillboardExistsFilter(), FSMBillboards.billboard_name)
async def choose_billboard_action(message: Message, state: FSMContext):

    await state.update_data(
        billboard_name=message.text.title()
    )

    data = await state.get_data()
    billboard = await get_billboard_info_by_name(data["billboard_name"])

    await state.set_state(FSMBillboards.choose_action)

    await message.answer(
        text=billboard
    )
    await message.answer(
        text="Выберите действие",
        reply_markup=change_billboard_data_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@billboards_router.message(F.text == "Назад", FSMBillboards.choose_action)
async def go_back_to_billboards_actions(message: Message, state: FSMContext):

    await state.set_state(FSMManagerPanel.billboards)

    await message.answer(
        text="Выберите действие",
        reply_markup=manager_billboards_actions_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@billboards_router.message(F.text, FSMBillboards.billboard_name)
async def process_unknown_billboard(message: Message):

    await message.answer(
        text="Билборда с таким названием нет в БД"
    )


@billboards_router.message(F.text == "Изменить цену", FSMBillboards.choose_action)
async def change_billboard_price(message: Message, state: FSMContext):

    await state.set_state(FSMBillboards.change_price)

    await message.answer(
        text="Введите новую цену"
    )


@billboards_router.message(F.text, FSMBillboards.change_price)
async def get_new_billboard_price(message: Message, state: FSMContext):

    data = await state.get_data()

    await state.set_state(FSMManagerPanel.start)
    await change_price(data["billboard_name"], message.text)

    await message.answer(
        text=f"Новая цена для билборда <b>{data['billboard_name']}</b> установлена - <b>{message.text}</b>",
        reply_markup=manager_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )
