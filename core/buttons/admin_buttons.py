from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

admin_set_manager_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

admin_set_manager_buttons_list = [
    InlineKeyboardButton(text="Назначить", callback_data="set_manager"),
    InlineKeyboardButton(text="Разжаловать", callback_data="unset_manager")
]

admin_set_manager_kb_builder.add(*admin_set_manager_buttons_list)
