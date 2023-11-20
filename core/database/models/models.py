from typing import List

from sqlalchemy import ForeignKey, Date
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship

from core.database.users.user_models import Base, User


class Billboard(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    width: Mapped[str] = mapped_column()
    height: Mapped[str] = mapped_column(String(50))
    sides: Mapped[int] = mapped_column()
    surface: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(50))
    pricePerDay: Mapped[float] = mapped_column()

    booking: Mapped[List["Booking"]] = relationship(back_populates="billboard")

    def __repr__(self):
        return "billboard " + self.id


class Order(Base):
    __tablename__ = "models"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    client_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    client: Mapped["User"] = relationship(back_populates="clientOrders")

    manager_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    manager: Mapped["User"] = relationship(back_populates="managerOrders")

    booking: Mapped[List["Booking"]] = relationship()

    def __repr__(self):
        return "billboard " + self.id


class Booking(Base):
    __tablename__ = "orders_billboards"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    order_id: Mapped[int] = (mapped_column(ForeignKey('orders.id')))
    order: Mapped["Order"] = relationship(back_populates="booking")

    billboard_id: Mapped[int] = (mapped_column(ForeignKey('models.id')))
    billboard: Mapped["Billboard"] = relationship(back_populates="booking")

    dateStart: Mapped[int] = mapped_column(Date)
    dateEnd: Mapped[int] = mapped_column(Date)
