from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext

from aiogram_calendar.simple_calendar import SimpleCalendar, SimpleCalendarCallback
from aiogram_calendar import get_user_locale

from core.buttons.create_booking_buttons import create_booking_end_kb_builder, create_booking_cancel_kb_builder
from core.database.models.db_models import Billboard, User, Order
from core.database.requests.billboards import get_billboards_by_district, get_billboard_by_name
from core.database.requests.booking import is_free_booking_period, create_booking
from core.database.requests.orders import get_order, create_order, delete_order
from core.database.requests.users import get_user

from core.states.states import FSMStart, FSMMakeOrder

from core.buttons.action_buttons import go_back_kb_builder, user_panel_kb_builder
from core.buttons.user_buttons import user_billboards_kb_builder, user_panel_about_us_kb_builder

from core.filters.billboard_filters import BillboardDistrictExists, BillboardExistsFilter
from core.utils.billboard_utils import get_billboard_info_by_name

order_router: Router = Router()


# 1
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


# Возвращение в главное меню пользователя
@order_router.message(F.text == "Назад", FSMStart.billboards)
async def go_back_to_main_menu(message: Message, state: FSMContext):
    print("назад в главное меню")
    await state.set_state(FSMStart.start)
    await message.answer(
        text=f'Здравствуйте, {message.from_user.username}!\nВыберите действие:',
        reply_markup=user_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


# 2
# Сохраняем билборд, пользователя и мэнеджера (создаем Order)
@order_router.message(BillboardExistsFilter(), FSMMakeOrder.choose_billboard)
async def start_date(message: Message, state: FSMContext):

    billboard: Billboard = await get_billboard_by_name(message.text)
    user: User = await get_user(message.from_user.id)
    cur_date = datetime.now()
    await state.update_data(
        choose_billboard=billboard.name,
        billboard_id=billboard.id,
        client_id=user.id,
        manager_id=user.manager_id,
        created_date=cur_date.strftime("%Y-%m-%d %H:%M:%S.%f"),
        created_date_y=int(cur_date.year),
        created_date_m=int(cur_date.month),
        created_date_d=int(cur_date.day),
        created_date_h=int(cur_date.hour),
        created_date_min=int(cur_date.minute),
        created_date_s=int(cur_date.second),
        created_date_ms=int(cur_date.microsecond)
    )

    await create_order(await state.get_data())
    booking_data = await state.get_data()
    order: Order = await get_order(user.id, user.manager_id, booking_data["created_date"])
    await state.update_data(
        order_id=order.id
    )

    await state.set_state(FSMMakeOrder.start_order)

    await message.answer(
        text="Выберите дату начала аренды: ",
        reply_markup=await SimpleCalendar(locale=await get_user_locale(
            message.from_user
        )).start_calendar()
    )


# Возвращение на выбор районов
@order_router.message(F.text == "Назад", FSMMakeOrder.choose_billboard)
async def go_back_to_select_district(message: Message, state: FSMContext):
    print("назад в выбор района")
    await state.set_state(FSMStart.billboards)
    await message.delete()
    await message.answer(
        text="Выберите район расположения билборда: ",
        reply_markup=user_billboards_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@order_router.message(F.text, FSMMakeOrder.choose_billboard)
async def process_unknown_billboard(message: Message):
    await message.answer(
        text="В выбранном районе нет билборда с таким названием!\n"
             "Напишите одно из названий выше"
    )



# 3
# Set start_date
@order_router.callback_query(SimpleCalendarCallback.filter(), FSMMakeOrder.start_order)
async def get_start_date(callback: CallbackQuery,
                         callback_data: CallbackData,
                         state: FSMContext):

    selected, date = await SimpleCalendar(locale=await get_user_locale(callback.from_user)).process_selection(
        callback, callback_data)

    if selected:
        month: int = date.month
        year: int = date.year

        await state.update_data(
            start_date=date.strftime("%Y-%m-%d"),
            start_date_y=date.year,
            start_date_m=date.month,
            start_date_d=date.day
        )

        await callback.message.delete()
        await state.set_state(FSMMakeOrder.end_date)
        await callback.message.answer(
            text=f'Дата начала аренды - {date.strftime("%Y-%m-%d")}')

        await callback.message.answer(
            text="Выберите дату конца аренды",
            reply_markup=await SimpleCalendar(locale=await get_user_locale(
                callback.from_user
            )).start_calendar(month=month, year=year)
        )


# 4
# Set end_date
@order_router.callback_query(SimpleCalendarCallback.filter(), FSMMakeOrder.end_date)
async def get_end_date(callback: CallbackQuery,
                       callback_data: CallbackData,
                       state: FSMContext):
    print("get_end_date")
    selected, date = await SimpleCalendar(locale=await get_user_locale(callback.from_user)).process_selection(
        callback, callback_data)

    if selected:

        await state.update_data(
            end_date=date.strftime("%Y-%m-%d"),
            end_date_y=date.year,
            end_date_m=date.month,
            end_date_d=date.day
        )
        booking_data: dict = await state.get_data()
        await callback.message.delete()
        await state.set_state(FSMMakeOrder.complete_order)

        is_free = await is_free_booking_period(billboard_id=booking_data["billboard_id"],
                                               date_start=booking_data["start_date"],
                                               date_end=booking_data["end_date"])

        await callback.message.answer(f'Дата конца аренды - {date.strftime("%Y-%m-%d")}')

        if is_free:  # если даты не заняты
            await create_booking(await state.get_data())
            await callback.message.answer(
                text="Билборд забронирован \nПродолжить бронирование билбордов?",
                reply_markup=create_booking_end_kb_builder.as_markup(
                    resize_keyboard=True
                )
            )
        else:  # если даты заняты
            await callback.message.answer(
                text="Данный период не доступен для бронирования. \nВыбрать другие даты?",
                reply_markup=create_booking_cancel_kb_builder.as_markup(
                    resize_keyboard=True
                )
            )


# @order_router.callback_query(F.data, FSMMakeOrder.free_period)
# async def free_period(callback: CallbackQuery, state: FSMContext):
#
#     await callback.message.answer(
#         text="Билборд забронирован \nПродолжить бронирование билбордов?",
#         reply_markup=create_booking_end_kb_builder.as_markup(
#             resize_keyboard=True
#         )
#     )
#
#
# @order_router.callback_query(F.data, FSMMakeOrder.not_free_period)
# async def not_free_period(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer(
#         text="Данный период не доступен для бронирования. \nВыбрать другие даты?",
#         reply_markup=create_booking_cancel_kb_builder.as_markup(
#             resize_keyboard=True
#         )
#     )


# Если букинг прошел удачно и нажата кнопка нет (завершить заказ)
@order_router.callback_query(F.data == 'booking_end', FSMMakeOrder.complete_order)
async def booking_end(callback: CallbackQuery, state: FSMContext):

    await state.set_state(FSMStart.start)
    await callback.message.delete()
    await callback.message.answer(
        text="Заказ сформирован",
        reply_markup=user_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


# Если букинг не прошел удачно и нажата кнопка нет (выбрать другой)
@order_router.callback_query(F.data == 'booking_cancel', FSMMakeOrder.complete_order)
async def booking_cancel(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await delete_order(state_data["order_id"])

    await state.set_state(FSMStart.billboards)
    await callback.message.delete()
    await callback.message.answer(
        text="заказ отменен",
        reply_markup=user_billboards_kb_builder.as_markup(
            resize_keyboard=True
        )
    )

