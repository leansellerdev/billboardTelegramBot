from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardButton


user_panel_about_us_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

about_us_buttons_user_panel = [
    "Контактная информация", "Связь с менеджером", "Назад"
]

user_panel_about_us_buttons: list[KeyboardButton] = [KeyboardButton(text=value) for value in about_us_buttons_user_panel]
user_panel_about_us_kb_builder.row(*user_panel_about_us_buttons, width=3)

