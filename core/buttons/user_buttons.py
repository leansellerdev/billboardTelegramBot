from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


user_panel_about_us_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
user_billboards_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()


about_us_buttons_user_panel = [
    "Контактная информация", "Связь с менеджером", "Назад"
]

user_billboards_buttons_list = [
    "Центр города", "Торговый центр", "Торговый квартал", "Назад"
]

user_panel_about_us_buttons: list[KeyboardButton] = [KeyboardButton(text=value) for
                                                     value in about_us_buttons_user_panel]
user_billboards_buttons: list[KeyboardButton] = [KeyboardButton(text=value) for
                                                 value in user_billboards_buttons_list]

user_panel_about_us_kb_builder.row(*user_panel_about_us_buttons, width=3)
user_billboards_kb_builder.row(*user_billboards_buttons, width=2)
