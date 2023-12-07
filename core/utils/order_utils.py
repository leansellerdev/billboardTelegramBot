import os

import pandas as pd

from core.database.requests.orders import *
from core.database.requests.booking import *
from core.database.models.db_models import Order, Booking
excel_path = "core/utils/temp/users.xlsx"


async def create_excel_to_send_user_order_bookings(bookings: list[Booking], total_price):

    data = []
    for i, booking in enumerate(bookings):

        dt = {
            "order_id": booking.order_id,
            "Название билборда": booking.billboard.name,
            "Дата начала": booking.dateStart.strftime("%Y-%m-%d"),
            "Конечная дата": booking.dateEnd.strftime("%Y-%m-%d"),
            "Цена": booking.price,
        }

        data.append(dt)

    tp = {
        "Цена": total_price
    }
    data.append(tp)

    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)

    return data


async def delete_excel_file():

    if not os.path.exists(excel_path):
        return

    os.remove(excel_path)

