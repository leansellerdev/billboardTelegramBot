from datetime import datetime

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback

from core.buttons.change_data_buttons import change_data_end_kb_builder
from core.buttons.user_buttons import user_panel_about_us_kb_builder, user_billboards_kb_builder
from core.buttons.action_buttons import user_panel_kb_builder
from core.database.requests.billboards import get_billboard_by_id
from core.database.requests.booking import get_order_bookings, get_booking_by_id, \
    is_free_booking_period_for_update, change_booking_date_end, change_booking_price
from core.database.requests.orders import get_orders_by_client_id

from core.database.requests.staff import get_manager_by_id
from core.database.requests.users import get_user_manager_id, get_user

from core.states.states import FSMStart, FSMMakeOrder, FSMSelfOrders

from core.utils.order_utils import get_order_info
from core.utils.price_utils import calculate_booking_price

users_router: Router = Router()


@users_router.message(F.text == "Мои заказы", FSMStart.start)
async def self_orders(message: Message, state: FSMContext):
    client = await get_user(message.from_user.id)
    orders = await get_orders_by_client_id(client.id)

    for order in orders:
        info = await get_order_info(order.id)
        await message.answer(
            text=info
        )
    await state.set_state(FSMSelfOrders.update_billboard)
    await message.answer(
        text="Введите номер заказа:"
    )


@users_router.message(F.text, FSMSelfOrders.update_billboard)
async def update_billboard(message: Message, state: FSMContext):
    await state.update_data(
        order_id=message.text
    )

    state_data = await state.get_data()

    bookings = await get_order_bookings(state_data["order_id"])
    text_bookings = ""
    for booking in bookings:
        text_bookings += (f"Номер бронирования: {booking.id} \nБилборд: {booking.billboard.name} "
                          f"\nДата начала: {booking.dateStart.strftime('%Y-%m-%d')} "
                          f"\nДата завершения: {booking.dateEnd.strftime('%Y-%m-%d')}")

    await message.answer(text=text_bookings)
    await message.answer(
        text="Введите номер бронирования:"
    )
    await state.set_state(FSMSelfOrders.billboard_id)


@users_router.message(F.text, FSMSelfOrders.billboard_id)
async def billboard_id(message: Message, state: FSMContext):
    booking = await get_booking_by_id(message.text)
    await state.update_data(
        booking_id=message.text,
        start_date=booking.dateStart.strftime('%Y-%m-%d'),
        billboard_id=booking.billboard_id,
        old_price=booking.price
    )

    await message.answer(
        text="Выберите дату конца аренды: ",
        reply_markup=await SimpleCalendar(locale=await get_user_locale(
            message.from_user
        )).start_calendar()
    )


@users_router.callback_query(SimpleCalendarCallback.filter(), FSMSelfOrders.billboard_id)
async def change_end_date(callback: CallbackQuery,
                          callback_data: CallbackData,
                          state: FSMContext):
    selected, date = await SimpleCalendar(locale=await get_user_locale(callback.from_user)).process_selection(
        callback, callback_data)

    if selected:
        await state.update_data(
            new_date_end=date.strftime("%Y-%m-%d")
        )
        state_data = await state.get_data()
        is_free = await is_free_booking_period_for_update(billboard_id=state_data["billboard_id"],
                                                          date_start=state_data["start_date"],
                                                          date_end=date.strftime("%Y-%m-%d"),
                                                          booking_id=state_data["booking_id"])
        await callback.message.answer(f'Новая дата конца аренды: {date.strftime("%Y-%m-%d")}')

        if is_free:  # если дата не занята
            billboard = await get_billboard_by_id(state_data["billboard_id"])
            days = abs(date.fromisoformat(date.strftime("%Y-%m-%d")) - date.fromisoformat(state_data["start_date"]))
            new_booking_price: float = await calculate_booking_price(billboard.pricePerDay, days.days + 1)

            await state.update_data(
                new_price=new_booking_price
            )

            old_price: float = state_data["old_price"]
            difference: float = new_booking_price - old_price
            message_text = ""
            if difference > 0:
                message_text = f"Дата может быть изменена\nДоплата: {difference:.2f}\nподтвердить операцию?"
            else:
                difference = difference * -1
                message_text = f"Дата может быть изменена\nЦена меньше на: {difference:.2f}\nподтвердить операцию?"

            await callback.message.answer(
                text=message_text,
                reply_markup=change_data_end_kb_builder.as_markup(
                    resize_keyboard=True
                )
            )
            await state.set_state(FSMSelfOrders.data_changed_end)
        else:  # если дата занята
            await callback.message.answer(
                text="Данный период не доступен для бронирования.\n"
                     "Введите номер заказа:",
            )
            await state.set_state(FSMSelfOrders.update_billboard)


@users_router.callback_query(F.data == 'change_data_end', FSMSelfOrders.data_changed_end)
async def change_data_end(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await change_booking_date_end(state_data["booking_id"], datetime.strptime(state_data["new_date_end"], '%Y-%m-%d'))
    await change_booking_price(state_data["booking_id"], state_data["new_price"])

    await state.set_state(FSMSelfOrders.update_billboard)
    await callback.message.answer(
        text="Сроки изменены. Ожидайте звонка менеджера\n"
             "Введите номер заказа:"
    )


@users_router.callback_query(F.data == 'cancel_change_data', FSMSelfOrders.data_changed_end)
async def change_data_end(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMSelfOrders.update_billboard)
    await callback.message.answer(
        text="Операция отменена\n"
             "Введите номер заказа:"
    )


@users_router.message(F.text == "Билборды", FSMStart.start)
async def billboards(message: Message, state: FSMContext):
    await state.set_state(FSMStart.billboards)
    await message.answer(
        text="Выберите район расположения билборда: ",
        reply_markup=user_billboards_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@users_router.callback_query(F.data == "booking_create_continue", FSMMakeOrder.complete_order)
async def billboards_(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStart.billboards)

    await callback.message.answer(
        text="Выберите район расположения билборда: ",
        reply_markup=user_billboards_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


@users_router.message(F.text == "О нас", FSMStart.start)
async def about_us(message: Message, state: FSMContext):
    await state.set_state(FSMStart.about)

    await message.answer(
        text="Выберите действие: ",
        reply_markup=user_panel_about_us_kb_builder.as_markup(resize_keyboard=True)
    )


@users_router.message(F.text == "Контактная информация", FSMStart.about)
async def contact_info(message: Message):
    await message.answer(
        text="Для связи с нами вы можете позвонить или написать по следующим номерам: "
             "\n+99999999999 \n+79993365542 \n+75936541258"
    )


@users_router.message(F.text == "Связь с менеджером", FSMStart.about)
async def communication_with_manager(message: Message):
    manager_id = await get_user_manager_id(message.from_user.id)
    manager = await get_manager_by_id(manager_id)

    # if not manager:
    #     await message.answer(
    #         text="Менеджер будет назначен после оформления первого заказа\n"
    #              "Вы можете связаться с нами по следующим номерам: \n"
    #              "\n+99999999999 \n+79993365542 \n+75936541258"
    #     )
    # else:
    await message.answer(
        text=f"Ваш менеджер: [{manager.name} {manager.surname}](tg://user?id={str(manager.telegram_id)})",
        parse_mode="Markdown"
    )


@users_router.message(F.text == "Назад", FSMStart.about)
async def go_back_to_user_menu(message: Message, state: FSMContext):
    await state.set_state(FSMStart.start)

    await message.answer(
        text="Выберите действие:",
        reply_markup=user_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )
