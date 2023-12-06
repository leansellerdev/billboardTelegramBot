import datetime
import os

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from core.database.models.db_models import Order

from core.database.requests.staff import basedir

from core.database.requests.staff import engine

session: Session(engine) = Session(engine)


async def create_order(order: dict):
    with session:
        order: Order = Order(
            client_id=order["client_id"],
            manager_id=order["manager_id"],
            created_date=datetime.datetime(order["created_date_y"], order["created_date_m"], order["created_date_d"],
                                           order["created_date_h"], order["created_date_min"], order["created_date_s"],
                                           order["created_date_ms"])
        )
        session.add(order)
        session.commit()


async def get_order(client_id, manager_id, created_date):
    with session:
        order: Order = session.query(Order).filter(
            Order.client_id == client_id,
            Order.manager_id == manager_id,
            Order.created_date == created_date).scalar()

    return order


async def delete_order(order_id):
    with session:
        session.query(Order).filter(Order.id == order_id).delete()
        session.commit()


# order = get_order(1, 1, '2023-12-06 22:25:52.583294')
# print(order.id)
# print(order.client_id)
# print(order.manager_id)
# print(order.created_date)













