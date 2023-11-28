import os

import pandas as pd

from core.database.requests.db_staff import (get_staff, create_staff,
                                             set_manager_status, delete_staff)
from core.database.models.db_models import User, Staff, Order
from creds import admins

excel_path = "core/utils/temp/users.xlsx"


async def is_admin(user_id):

    if user_id not in admins:
        return False

    return True


async def is_manager(user_id: str):

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


async def get_user_info(user_id):

    user_data = await get_user(user_id)

    user_info = {
        "Имя": user_data.name,
        "Фамилия": user_data.surname,
        "Почта": user_data.email,
        "Номер телефона": user_data.phone_number
    }

    text_to_send = ""

    for key, value in user_info.items():
        text_to_send += f"{key}: {value}\n"

    return text_to_send


async def create_excel_to_send(users: list[User, Staff]):

    data = []

    for i, user in enumerate(users):

        dt = {
            "id": user.telegram_id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "phone_number": user.phone_number,
            "status_isManager": user.isManager
        }

        data.append(dt)

    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)

    return data


async def create_excel_to_send_manager_orders(orders: list[Order]):

    data = []

    for i, order in enumerate(orders):

        dt = {
            "client": order.client.telegram_id,
            "manager": order.manager.telegram_id,
            "orders": order.booking,
        }

        data.append(dt)

    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)

    return data


async def delete_excel_file():

    if not os.path.exists(excel_path):
        return

    os.remove(excel_path)

