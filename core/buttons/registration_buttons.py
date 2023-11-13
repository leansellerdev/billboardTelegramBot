from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


reg_end_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

reg_end_buttons_list = [
    InlineKeyboardButton(text="Да", callback_data="reg_end"),
    InlineKeyboardButton(text="Изменить данные", callback_data="change_data")
]

reg_end_kb_builder.add(*reg_end_buttons_list)
