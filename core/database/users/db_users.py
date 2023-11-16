import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from core.database.users.user_models import User

basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine(f"sqlite:///{os.path.join(basedir, '../database.db')}", echo=True)
session: Session(engine) = Session(engine)


async def create_user(user: dict):

    with session:
        user: User = User(
            telegram_id=user["tg_id"],
            name=user["name"],
            surname=user["surname"],
            email=user["email"],
            phone_number=user["phone_number"].replace(" ", "")
        )

        session.add(user)

        session.commit()


async def get_user(user_id: int):

    user = session.query(User).filter(User.telegram_id == user_id).scalar()

    return user


async def change_user_phone(user_id: int, new_phone_number):

    with session:
        user = session.scalar(select(User).filter_by(telegram_id=user_id))
        user.phone_number = new_phone_number

        session.commit()


async def change_user_email(user_id: int, new_email_address: str):

    with session:
        user = session.scalar(select(User).filter_by(telegram_id=user_id))
        user.email = new_email_address

        session.commit()
