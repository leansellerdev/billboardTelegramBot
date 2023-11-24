from core.database.requests.db_staff import get_staff


async def is_admin(staff_id):
    user_exists = await get_staff(staff_id)
    if not user_exists:
        return False
    return True
