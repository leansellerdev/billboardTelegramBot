import os

import pandas as pd

from core.database.models.db_models import Staff
from core.database.requests.users import *

from creds import admins


excel_path = "core/utils/temp/users.xlsx"


async def user_registered(user_id):

    user_exists = await get_user(user_id)

    if not user_exists:
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


async def create_excel_to_send_manager_users(users: list[User, Staff]):

    data = []

    for i, user in enumerate(users):

        dt = {
            "id": user.telegram_id,
            "имя": user.name,
            "фамилия": user.surname,
            "почта": user.email,
            "номер телефона": user.phone_number
        }

        data.append(dt)

    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)

    return data


async def delete_excel_file():

    if not os.path.exists(excel_path):
        return

    os.remove(excel_path)
