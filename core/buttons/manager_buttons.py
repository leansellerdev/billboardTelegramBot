from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardButton


manager_panel_statistics_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
manager_clients_actions_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
manager_billboards_actions_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()


statistics_buttons_manager_panel = [
    "Ст-ка по билборду", "Ст-ка всех билбордов", "Назад"
]

billboards_actions: list = [
    "Изменить биллборд", "Добавить биллборд", "Назад"
]

clients_actions_buttons: list[InlineKeyboardButton] = [
    InlineKeyboardButton(text="Список клиентов", callback_data="clients_list"),
    InlineKeyboardButton(text="Назначенные заказы", callback_data="orders")
]

manager_panel_statistics_buttons: list[KeyboardButton] = [
    KeyboardButton(text=value) for value in statistics_buttons_manager_panel
]

billboards_actions_buttons: list[KeyboardButton] = [
    KeyboardButton(text=value) for value in billboards_actions
]

manager_panel_statistics_kb_builder.row(*manager_panel_statistics_buttons, width=2)
manager_billboards_actions_kb_builder.row(*billboards_actions_buttons, width=2)
manager_clients_actions_kb_builder.add(*clients_actions_buttons)
