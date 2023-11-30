from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


change_billboard_data_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

change_billboard_data: list = [
    "Изменить цену", "Назад"
]

change_billboard_data_buttons: list[KeyboardButton] = [KeyboardButton(text=value) for value in change_billboard_data]

change_billboard_data_kb_builder.row(*change_billboard_data_buttons, width=3)
