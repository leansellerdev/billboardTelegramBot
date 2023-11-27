import os
from sqlalchemy import select, create_engine

from core.database.models.db_models import Staff, User
from sqlalchemy.orm import Session
# from core.database.requests.db_users import engine

basedir = r"C:\Users\ddudk\Desktop\pycharmprojects\billboardTelegramBot"

engine = create_engine(f"sqlite:///{os.path.join(basedir, 'database.db')}", echo=True)
session: Session = Session(engine)


async def create_staff(staff: dict):

    with session:
        staff: Staff = Staff(
            telegram_id=staff["telegram_id"],
            name=staff["name"],
            surname=staff["surname"],
            email=staff["email"],
            phone_number=staff["phone_number"],
            isManager=staff["isManager"]
        )
        session.add(staff)
        session.commit()


async def get_staff(staff_id: str):

    staff: Staff = session.query(Staff).filter(Staff.telegram_id == staff_id).scalar()
    return staff


async def delete_staff(staff_id: str):

    with session:

        staff: Staff = session.scalar(select(Staff).filter_by(telegram_id=staff_id))
        session.delete(staff)

        session.commit()


async def get_all_managers():

    staffs = session.query(Staff).filter(Staff.isManager == 1).all()
    return staffs


async def change_staff_phone(staff_id: int, new_phone_number):

    with session:

        staff: Staff = session.scalar(select(Staff).filter_by(telegram_id=staff_id))
        staff.phone_number = new_phone_number
        session.commit()


async def change_staff_email(staff_id: int, new_email_address: str):

    with session:

        staff: Staff = session.scalar(select(Staff).filter_by(telegram_id=staff_id))
        staff.email = new_email_address
        session.commit()


async def set_manager_status(user_id: str, status: bool):

    with session:

        user: User = session.scalar(select(User).filter_by(telegram_id=user_id))
        user.isManager = status

        staff_info = {
            "telegram_id": user.telegram_id,
            "name": user.name,
            'surname': user.surname,
            'email': user.email,
            'phone_number': user.phone_number,
            'isManager': user.isManager
        }

        session.commit()

    return staff_info

# set_manager_status("889767148", True)
