from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


change_data_end_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

create_billboard_end_buttons_list = [
    InlineKeyboardButton(text="Выполнить", callback_data="change_data_end"),
    InlineKeyboardButton(text="Отмена", callback_data="cancel_change_data")
]

change_data_end_kb_builder.add(*create_billboard_end_buttons_list)
