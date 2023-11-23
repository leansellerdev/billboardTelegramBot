import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from core.database.models.db_models import Staff
from core.database.db_users import engine, session


async def create_staff(staff: dict):

    with session:
        staff: Staff = Staff(
            telegram_id=staff["tg_id"],
            name=staff["name"],
            surname=staff["surname"],
            email=staff["email"],
            phone_number=staff["phone_number"].replace(" ", "")
        )
        session.add(staff)
        session.commit()


async def get_staff(staff_id: int):
    staff = session.query(Staff).filter(Staff.telegram_id == staff_id).scalar()
    return staff


async def change_staff_phone(staff_id: int, new_phone_number):
    with session:
        staff = session.scalar(select(Staff).filter_by(telegram_id=staff_id))
        staff.phone_number = new_phone_number
        session.commit()


async def change_staff_email(staff_id: int, new_email_address: str):
    with session:
        staff = session.scalar(select(Staff).filter_by(telegram_id=staff_id))
        staff.email = new_email_address
        session.commit()
