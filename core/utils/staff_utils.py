import os

import pandas as pd

from core.database.requests.staff import (get_staff, create_staff,
                                          set_manager_status, delete_staff)
from core.database.models.db_models import User, Staff, Order
from creds import admins

excel_path = "core/utils/temp/users.xlsx"


async def is_admin(user_id):

    if user_id not in admins:
        return False

    return True


async def is_manager(user_id):

    if not await get_staff(user_id):
        return False

    return True


async def set_manager(user_id: str, status: bool):

    staff = await set_manager_status(user_id, status)

    if status:
        await create_staff(staff)
    else:
        await delete_staff(user_id)


async def id_valid(user_id: str):

    if not len(user_id) == 9 and not user_id.isdigit():
        return False

    return True


async def create_excel_to_send(users: list[User, Staff]):

    data = []

    for i, user in enumerate(users):

        dt = {
            "id": user.telegram_id,
            "имя": user.name,
            "фамилия": user.surname,
            "почта": user.email,
            "номер телефона": user.phone_number,
        }

        data.append(dt)

    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)

    return data


async def create_excel_to_send_manager_orders(orders: list[Order]):

    data = []

    for i, order in enumerate(orders):

        # dt = {
        #     "номер заказа:": order.id,
        #     "клиент": order.client.telegram_id,
        #     "менеджер": order.manager.telegram_id,
        # }

        # data.append(dt)

        # bookings = {
        #     "номер заказа": "",
        #     "билборд": "",
        #     "дата начала": "",
        #     "дата конца": "",
        # }

        for booking in order.booking:
            bookings = {
                "номер заказа:": order.id,
                "клиент": order.client.telegram_id,
                "менеджер": order.manager.telegram_id,
                "номер бронирования": booking.id,
                "билборд": booking.billboard.name,
                "дата начала": booking.dateStart,
                "дата конца": booking.dateEnd,
                "цена": booking.price,
            }
            data.append(bookings)

    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)

    return data


async def delete_excel_file():

    if not os.path.exists(excel_path):
        return

    os.remove(excel_path)

