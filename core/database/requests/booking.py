import datetime
import os

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from core.database.models.db_models import Billboard, Booking

from core.database.requests.staff import basedir

from core.database.requests.staff import engine

session: Session(engine) = Session(engine)


async def create_booking(booking: dict):
    with session:
        booking: Booking = Booking(
            order_id=booking["order_id"],
            billboard_id=booking["billboard_id"],
            dateStart=datetime.datetime(booking["start_date_y"], booking["start_date_m"], booking["start_date_d"]),
            dateEnd=datetime.datetime(booking["end_date_y"], booking["end_date_m"], booking["end_date_d"])
        )
        session.add(booking)
        session.commit()


async def is_free_booking_period(billboard_id, date_start, date_end):
    with (session):
        bookings: list[[Booking]] = session.query(Booking).filter(Booking.billboard_id == billboard_id).filter(
            ((Booking.dateStart >= date_start) & (Booking.dateStart <= date_end)) |
            ((Booking.dateEnd >= date_start) & (Booking.dateEnd <= date_end))
        ).all()
        print(date_start)
        print(date_end)
        print("33333333333333333333333333333333 LEN:")
        print(len(bookings))
        if len(bookings) | bool(bookings):
            return False
        else:
            return True


