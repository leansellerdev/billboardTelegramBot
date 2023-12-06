from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


create_booking_end_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
create_booking_cancel_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

create_booking_end_buttons_list = [
    InlineKeyboardButton(text="Да", callback_data="booking_create_continue"),
    InlineKeyboardButton(text="Нет (Завершить заказ)", callback_data="booking_end")
]

create_booking_cancel_buttons_list = [
    InlineKeyboardButton(text="Да", callback_data="booking_change_date"),
    InlineKeyboardButton(text="Нет (выбрать другой билборд)", callback_data="booking_cancel")
]

create_booking_end_kb_builder.add(*create_booking_end_buttons_list)
create_booking_cancel_kb_builder.add(*create_booking_cancel_buttons_list)
