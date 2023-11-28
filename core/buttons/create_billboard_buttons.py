from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


create_billboard_end_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

create_billboard_end_buttons_list = [
    InlineKeyboardButton(text="Да", callback_data="billboard_create_end"),
    InlineKeyboardButton(text="Отменить создание", callback_data="cancel_billboard_create")
]

create_billboard_end_kb_builder.add(*create_billboard_end_buttons_list)
