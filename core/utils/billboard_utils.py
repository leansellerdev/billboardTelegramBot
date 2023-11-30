from core.database.requests.billboards import get_billboard_by_name
from core.database.models.db_models import Billboard


async def get_billboard_info_by_name(billboard_name: str) -> str:

    billboard_data: Billboard = await get_billboard_by_name(billboard_name)

    billboard_info = {
        "Название": billboard_data.name,
        "Ширина": billboard_data.width,
        "Высота": billboard_data.height,
        "Стороны": billboard_data.sides,
        "Тип": billboard_data.surface,
        "Адрес": billboard_data.address,
        "Цена за день": billboard_data.pricePerDay
    }

    text_to_send = ""

    for key, value in billboard_info.items():
        text_to_send += f"{key}: {value}\n"

    return text_to_send


async def billboard_exists(billboard_name: str) -> bool:

    if not await get_billboard_by_name(billboard_name):
        return False

    return True
