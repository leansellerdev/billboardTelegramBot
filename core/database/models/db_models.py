from typing import List

import datetime
from sqlalchemy import ForeignKey, Date, Boolean, DateTime
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
# from core.database.db_users import engine

# from core.database.db_users import engine


class Base(DeclarativeBase):
    pass


class Billboard(Base):
    __tablename__ = "billboards"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(50))
    width: Mapped[str] = mapped_column(String(50))
    height: Mapped[str] = mapped_column(String(50))
    sides: Mapped[str] = mapped_column(String(50))
    surface: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(255))
    pricePerDay: Mapped[float] = mapped_column()

    booking: Mapped[List["Booking"]] = relationship(back_populates="billboard")

    def __repr__(self):
        return f"Billboard(id={self.id!r}), name={self.name!r}, surface={self.surface!r}, address={self.address!r}, " \
               f"pricePerDay={self.pricePerDay!r}"


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    client: Mapped["User"] = relationship('User', back_populates="orders", foreign_keys=[client_id])
    manager_id: Mapped[int] = mapped_column(ForeignKey("staff.id"))
    manager: Mapped["Staff"] = relationship('Staff', back_populates="orders", foreign_keys=[manager_id])
    booking: Mapped[List["Booking"]] = relationship()
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))
    total_price: Mapped[float] = mapped_column()

    def __repr__(self):
        return self.id


class Booking(Base):
    __tablename__ = "orders_billboards"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    order_id: Mapped[int] = (mapped_column(ForeignKey('orders.id')))
    order: Mapped["Order"] = relationship(back_populates="booking")

    billboard_id: Mapped[int] = (mapped_column(ForeignKey('billboards.id')))
    billboard: Mapped["Billboard"] = relationship(back_populates="booking")

    dateStart: Mapped[int] = mapped_column(Date)
    dateEnd: Mapped[int] = mapped_column(Date)
    price: Mapped[float] = mapped_column()


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[int] = mapped_column()

    isManager: Mapped[bool] = mapped_column(Boolean, unique=False, default=0)
    # isAdmin: Mapped[bool] = mapped_column(Boolean, unique=False, default=0)

    orders: Mapped[List["Order"]] = relationship()
    manager_id: Mapped[int] = mapped_column(ForeignKey('staff.id'), nullable=True)

    def __repr__(self):
        return f"User(id={self.id!r}), name={self.name!r}, surname={self.surname!r}, email={self.email!r}"


class Staff(Base):

    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[int] = mapped_column()

    isManager: Mapped[bool] = mapped_column(Boolean, unique=False, default=False)
    # isAdmin: Mapped[bool] = mapped_column(Boolean, unique=False, default=False)

    orders: Mapped[List["Order"]] = relationship()
    users: Mapped[List["User"]] = relationship()

    def __repr__(self):
        return (f"User(id={self.id!r}), name={self.name!r}, surname={self.surname!r}, email={self.email!r}, "
                f"isManager={self.isManager!r}")

    def return_is_manager(self):
        return self.isManager


















