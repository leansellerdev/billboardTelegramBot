from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship

from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)

    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(50))

    email: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[int] = mapped_column()

    def __repr__(self):
        return f"User(id={self.id!r}), name={self.name!r}, surname={self.surname!r}, email={self.email!r}"
