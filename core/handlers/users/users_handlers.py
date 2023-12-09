from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from core.buttons.user_buttons import user_panel_about_us_kb_builder, user_billboards_kb_builder
from core.buttons.action_buttons import user_panel_kb_builder
from core.database.requests.booking import get_order_bookings
from core.database.requests.orders import get_orders_by_client_id

from core.database.requests.staff import get_manager_by_id
from core.database.requests.users import get_user_manager_id, get_user
from core.database.requests.billboards import get_billboards_by_district

from core.states.states import FSMStart, FSMMakeOrder, FSMSelfOrders

from core.filters.billboard_filters import BillboardDistrictExists
from core.utils.billboard_utils import get_billboard_info_by_name
from core.utils.order_utils import get_order_info

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
        text_bookings += f"Номер билборда: {booking.billboard_id} \nНазвание: {booking.billboard.name}\n"

    await message.answer(text=text_bookings)
    await message.answer(
        text="Введите номер билборда:"
    )
    await state.set_state(FSMSelfOrders.billboard_id)


@users_router.message(F.text, FSMSelfOrders.billboard_id)
async def billboard_id(message: Message, state: FSMContext):
    await state.update_data(
        billboard_id=message.text
    )



    #await state.set_state(FSMSelfOrders.billboard_id)
    await message.answer(
        text="ssss"
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

