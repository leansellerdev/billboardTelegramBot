from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


registered_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
not_registered_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
admin_panel_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

cancel_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
go_back_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

start_buttons_registered = [
    "Мои заказы", "Биллборды", "О нас"
]

start_buttons_not_registered = [
    "Регистрация", "Биллборды", "О нас"
]

start_buttons_admin_panel = [
    "Пользователи", "Управление персоналом", "Заказы"
]

cancel_button = KeyboardButton(text="Отмена")
go_back_button = KeyboardButton(text="Назад")

registered_buttons: list[KeyboardButton] = [KeyboardButton(text=value) for value in start_buttons_registered]
not_registered_buttons: list[KeyboardButton] = [KeyboardButton(text=value) for value in start_buttons_not_registered]
admin_panel_buttons: list[KeyboardButton] = [KeyboardButton(text=value) for value in start_buttons_admin_panel]

registered_kb_builder.row(*registered_buttons, width=3)
not_registered_kb_builder.row(*not_registered_buttons, width=3)
admin_panel_kb_builder.row(*admin_panel_buttons, width=3)

cancel_kb_builder.add(cancel_button)
go_back_kb_builder.add(go_back_button)
