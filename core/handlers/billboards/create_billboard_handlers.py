from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from core.buttons.action_buttons import manager_panel_kb_builder
from core.buttons.create_billboard_buttons import create_billboard_end_kb_builder
from core.database.requests.billboards import create_billboard
from core.states.states import FSMCreateBillboard, FSMManagerPanel, FSMStart
from core.utils.billboard_utils import get_billboard_info_by_name

create_billboard_router: Router = Router()


# Successful create billboard
@create_billboard_router.callback_query(F.data == "billboard_create_end", FSMCreateBillboard.end)
async def billboard_create(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await create_billboard(billboard=data)

    await state.set_state(FSMStart.start)

    await callback.answer(
        text="Билборд создан!",
        show_alert=True
    )

    billboard_info = await get_billboard_info_by_name(data["name"])  # data.get("id", None)

    await callback.message.delete()
    await callback.message.answer(
        text=billboard_info,
        reply_markup=manager_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


# Change user data
@create_billboard_router.callback_query(F.data == 'cancel_billboard_create', FSMCreateBillboard.end)
async def change_billboard_date(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await callback.message.answer(
        text="Создание билборда отменено",
        reply_markup=manager_panel_kb_builder.as_markup(
            resize_keyboard=True
        )
    )


# 1. Enter width
# @create_billboard_router.message(Command(commands=["registration"]))
@create_billboard_router.message(F.text == "Добавить билборд", FSMManagerPanel.billboards)
async def enter_width(message: Message, state: FSMContext):

    await state.set_state(FSMCreateBillboard.width)
    await message.answer(
        text="Введите ширину\n\n",
        reply_markup=ReplyKeyboardRemove()
    )


# 2. Enter height
@create_billboard_router.message(F.text, FSMCreateBillboard.width)
async def enter_height(message: Message, state: FSMContext):

    await state.update_data(
        width=message.text
        )

    await state.set_state(FSMCreateBillboard.height)
    await message.answer(
        text="Введите высоту"
    )


# 3. Enter sides
@create_billboard_router.message(F.text, FSMCreateBillboard.height)
async def enter_sides(message: Message, state: FSMContext):

    await state.update_data(
        height=message.text
    )

    await state.set_state(FSMCreateBillboard.sides)
    await message.answer(
        text="Введите кол-во сторон"
    )


# 4. Enter surface
@create_billboard_router.message(FSMCreateBillboard.sides)
async def enter_surface(message: Message, state: FSMContext):

    await state.update_data(
        sides=message.text
    )

    await state.set_state(FSMCreateBillboard.surface)
    await message.answer(
        text="Введите поверхность"
    )


# 5. Enter address
@create_billboard_router.message(FSMCreateBillboard.surface)
async def enter_address(message: Message, state: FSMContext):

    await state.update_data(
        surface=message.text
    )

    await state.set_state(FSMCreateBillboard.address)
    await message.answer(
        text="Введите адрес"
    )


# 6. Enter pricePerDay
@create_billboard_router.message(FSMCreateBillboard.address)
async def enter_price_per_day(message: Message, state: FSMContext):

    await state.update_data(
        address=message.text
    )

    await state.set_state(FSMCreateBillboard.pricePerDay)
    await message.answer(
        text="Введите цену аренды за день"
    )


# 7. Create last step
@create_billboard_router.message(FSMCreateBillboard.pricePerDay)
async def billboard_create_ending(message: Message, state: FSMContext):

    await state.update_data(
        pricePerDay=message.text
    )
    await state.set_state(FSMCreateBillboard.end)
    await message.answer(
        text="Завершить создание?",
        reply_markup=create_billboard_end_kb_builder.as_markup(
            resize_keyboard=True
        )
    )

