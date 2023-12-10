import os

import pandas as pd

from core.database.requests.billboards import get_billboard_by_name, get_billboards_by_district
from core.database.models.db_models import Billboard

excel_path = "core/utils/temp/users.xlsx"


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


async def billboard_district_exists(district: str) -> bool:

    if not await get_billboards_by_district(district):
        return False

    return True


async def create_excel_to_send_all_billboards(billboards: list[Billboard]):

    data = []

    for i, billboard in enumerate(billboards):

        dt = {
            "название": billboard.name,
            "ширина": billboard.width,
            "высота": billboard.height,
            "покрытие": billboard.surface,
            "стороны": billboard.sides,
            "адрес": billboard.address,
            "цена": billboard.pricePerDay
        }

        data.append(dt)

    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)

    return data


async def delete_excel_file():

    if not os.path.exists(excel_path):
        return

    os.remove(excel_path)
