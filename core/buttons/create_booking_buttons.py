from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


create_booking_end_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
create_booking_cancel_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
create_order_end_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

create_booking_end_buttons_list = [
    InlineKeyboardButton(text="Да", callback_data="booking_create_continue"),
    InlineKeyboardButton(text="Нет (Завершить заказ)", callback_data="booking_end")
]

create_booking_cancel_buttons_list = [
    InlineKeyboardButton(text="Да", callback_data="booking_change_date"),
    InlineKeyboardButton(text="Выбрать другой билборд", callback_data="booking_cancel")
]

complete_order_buttons_list = [
    InlineKeyboardButton(text="Оформить заказ", callback_data="order_complete_end"),
    InlineKeyboardButton(text="Отменить заказ", callback_data="order_complete_cancel")
]


create_booking_end_kb_builder.add(*create_booking_end_buttons_list)
create_booking_cancel_kb_builder.add(*create_booking_cancel_buttons_list)
create_order_end_kb_builder.add(*complete_order_buttons_list)