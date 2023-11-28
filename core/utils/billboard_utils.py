from core.database.requests.db_billboards import get_billboard


async def get_billboard_info(billboard_id: str):

    billboard_data = await get_billboard(billboard_id)

    billboard_info = {
        "Ширина": billboard_data.width,
        "Высота": billboard_data.height,
        "Стороны": billboard_data.sides,
        "Материал": billboard_data.surface,
        "Адрес": billboard_data.address,
        "Цена за день": billboard_data.pricePerDay
    }

    text_to_send = ""

    for key, value in billboard_info.items():
        text_to_send += f"{key}: {value}\n"

    return text_to_send

