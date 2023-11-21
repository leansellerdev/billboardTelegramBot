from core.database.db_users import get_user


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
