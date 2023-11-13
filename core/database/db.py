from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.database.user_models import User

engine = create_engine("sqlite+pysqlite:///core/database/database.db", echo=True)
session: Session(engine) = Session(engine)


async def create_user(user_id, name, surname, email, phone_number):

    with session:
        user: User = User(
            telegram_id=user_id,
            name=name,
            surname=surname,
            email=email,
            phone_number=phone_number
        )

        session.add(user)

        session.commit()
