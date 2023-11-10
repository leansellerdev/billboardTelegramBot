from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


registered_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
not_registered_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

start_buttons_registered = [
    "Мои заказы", "Биллборды", "О нас"
]

start_buttons_not_registered = [
    "Регистрация", "Биллборды", "О нас"
]

registered_buttons: list[KeyboardButton] = [KeyboardButton(text=value) for value in start_buttons_registered]
not_registered_buttons: list[KeyboardButton] = [KeyboardButton(text=value) for value in start_buttons_not_registered]

registered_kb_builder.row(*registered_buttons, width=3)
not_registered_kb_builder.row(*not_registered_buttons, width=3)
