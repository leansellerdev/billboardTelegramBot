import datetime
import os

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session, subqueryload

from core.database.models.db_models import Order, Booking

from core.database.requests.staff import engine

session: Session(engine) = Session(engine)


async def create_order(order: dict):
    with session:
        order: Order = Order(
            client_id=order["client_id"],
            manager_id=order["manager_id"],
            created_date=datetime.datetime(order["created_date_y"], order["created_date_m"], order["created_date_d"],
                                           order["created_date_h"], order["created_date_min"], order["created_date_s"],
                                           order["created_date_ms"]),
            total_price=order["total_price"]
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


async def get_order_by_id(order_id):
    with session:
        order: Order = session.query(Order).options(subqueryload(Order.booking)).filter(
            Order.id == order_id).scalar()

    return order


async def get_orders_by_client_id(client_id):
    with session:
        orders: list[[Order]] = session.query(Order).filter(
            Order.client_id == client_id).options(subqueryload(Order.booking)).all()

    return orders


async def update_order_total_price(order_id, total_price):
    order = session.scalar(select(Order).filter_by(id=order_id))
    order.phone_number = total_price

    session.commit()


async def delete_order(order_id):
    with session:
        session.query(Order).filter(Order.id == order_id).delete()
        session.commit()


# order = get_order(1, 1, '2023-12-06 22:25:52.583294')
# print(order.id)
# print(order.client_id)
# print(order.manager_id)
# print(order.created_date)













