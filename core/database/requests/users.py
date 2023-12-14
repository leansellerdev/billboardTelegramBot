import os

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from core.database.models.db_models import User

from core.database.requests.staff import engine

session: Session(engine) = Session(engine)


async def create_user(user: dict):

    with session:
        user: User = User(
            telegram_id=user["tg_id"],
            name=user["name"].title(),
            surname=user["surname"].title(),
            email=user["email"],
            phone_number=user["phone_number"].replace(" ", ""),
            manager_id=user["manager_id"]
        )

        session.add(user)

        session.commit()


async def get_user(user_id: int):
    with session:
        user: User = session.query(User).filter(User.telegram_id == user_id).scalar()

    return user


async def get_user_manager_id(user_id: int):
    with session:
        user = session.query(User).filter(User.telegram_id == user_id).scalar()

    return user.manager_id


async def get_user_manager_id(user_id: int):
    with session:
        user = session.query(User).filter(User.telegram_id == user_id).scalar()

    return user.manager_id


async def change_user_phone(user_id: int, new_phone_number):

    user = session.scalar(select(User).filter_by(telegram_id=user_id))
    user.phone_number = new_phone_number

    session.commit()


async def change_user_email(user_id: int, new_email_address: str):

    user = session.scalar(select(User).filter_by(telegram_id=user_id))
    user.email = new_email_address

    session.commit()


async def get_all_users():

    with session:
        users: list[[User]] = session.query(User).all()

    return users

