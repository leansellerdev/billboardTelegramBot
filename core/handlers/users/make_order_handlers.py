from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext

from aiogram_calendar.simple_calendar import SimpleCalendar, SimpleCalendarCallback
from aiogram_calendar import get_user_locale

from core.database.requests.billboards import get_billboards_by_district

from core.states.states import FSMStart, FSMMakeOrder

from core.buttons.action_buttons import go_back_kb_builder
from core.buttons.user_buttons import user_billboards_kb_builder

from core.filters.billboard_filters import BillboardDistrictExists, BillboardExistsFilter
from core.utils.billboard_utils import get_billboard_info_by_name

order_router: Router = Router()


@order_router.message(BillboardDistrictExists(), FSMStart.billboards)
async def choose_billboard(message: Message, state: FSMContext):
    await state.set_state(FSMMakeOrder.choose_billboard)

    billboards = await get_billboards_by_district(message.text)

    for billboard in billboards:
        info = await get_billboard_info_by_name(billboard.name)

        await message.answer(
            text=info
        )

    await message.answer(
        text="Для начала оформления заказа введите название билборда",
        reply_markup=go_back_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@order_router.message(F.text == "Назад", FSMMakeOrder.choose_billboard)
async def go_back_to_main_menu(message: Message, state: FSMContext):
    await state.set_state(FSMStart.billboards)

    await message.answer(
        text="Выберите район расположения билборда: ",
        reply_markup=user_billboards_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@order_router.message(BillboardExistsFilter(), FSMMakeOrder.choose_billboard)
async def start_date(message: Message, state: FSMContext):
    await state.set_state(FSMMakeOrder.start_order)

    await message.answer(
        text="Выберите дату начала аренды: ",
        reply_markup=await SimpleCalendar(locale=await get_user_locale(
            message.from_user
        )).start_calendar()
    )


@order_router.message(F.text, FSMMakeOrder.choose_billboard)
async def process_unknown_billboard(message: Message):
    await message.answer(
        text="В выбранном районе нет билборда с таким названием!\n"
             "Напишите одно из названий выше"
    )


@order_router.callback_query(SimpleCalendarCallback.filter(), FSMMakeOrder.start_order)
async def get_start_date(callback: CallbackQuery,
                         callback_data: CallbackData,
                         state: FSMContext):
    selected, date = await SimpleCalendar(locale=await get_user_locale(callback.from_user)).process_selection(
        callback, callback_data)

    if selected:
        month: int = date.month
        year: int = date.year

        await callback.message.delete()

        await state.set_state(FSMMakeOrder.end_date)
        await callback.message.answer(
            text=f'Дата начала аренды - {date.strftime("%d.%m.%Y")}')

        await callback.message.answer(
            text="Выберите дату конца аренды",
            reply_markup=await SimpleCalendar(locale=await get_user_locale(
                callback.from_user
            )).start_calendar(month=month, year=year)
        )


@order_router.callback_query(SimpleCalendarCallback.filter(), FSMMakeOrder.end_date)
async def get_end_date(callback: CallbackQuery,
                       callback_data: CallbackData,
                       state: FSMContext):
    selected, date = await SimpleCalendar(locale=await get_user_locale(callback.from_user)).process_selection(
        callback, callback_data)

    if selected:
        await callback.message.delete()

        await state.set_state(FSMMakeOrder.complete_order)
        await callback.message.answer(
            f'Дата конца аренды - {date.strftime("%d.%m.%Y")}')
