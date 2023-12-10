from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext

from core.states.states import FSMStart, FSMManagerPanel, FSMAdminPanel
from core.buttons.action_buttons import (not_registered_kb_builder,
                                         user_panel_kb_builder, admin_panel_kb_builder, manager_panel_kb_builder)

from core.utils.users_utils import user_registered
from core.utils.staff_utils import *


router: Router = Router()


@router.message(CommandStart())
@router.message(Command(commands=["cancel"]))
@router.message(F.text == "Отмена", F.text == "Назад")
async def start(message: Message, state: FSMContext):
    username = message.from_user.first_name

    # if await is_admin(message.from_user.id):
    #     await state.set_state(FSMAdminPanel.start)
    #
    #     await message.answer(
    #         text=f'Здравствуйте Администратор, {username}!\nВыберите действие:',
    #         reply_markup=admin_panel_kb_builder.as_markup(
    #             resize_keyboard=True
    #         )
    #     )
    # elif await is_manager(message.from_user.id):
    #     await state.set_state(FSMManagerPanel.start)
    #
    #     await message.answer(
    #         text=f'Здравствуйте Менеджер, {username}!\nВыберите действие:',
    #         reply_markup=manager_panel_kb_builder.as_markup(
    #             resize_keyboard=True
    #         )
    #     )
    if not await user_registered(message.from_user.id):
        await state.set_state(FSMStart.start)

        await message.answer(
            text=f'Здравствуйте, {username}!\n\n'
                 f'Для доступа к полному функционалу Вам необходимо зарегистрироваться - /registration',
            reply_markup=not_registered_kb_builder.as_markup(
                resize_keyboard=True
            )
        )
    else:
        await state.set_state(FSMStart.start)

        await message.answer(
            text=f'Здравствуйте, {username}!\nВыберите действие:',
            reply_markup=user_panel_kb_builder.as_markup(
                resize_keyboard=True
            )
        )
