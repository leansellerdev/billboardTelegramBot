from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database.models.db_models import Billboard

from .staff import engine

session: Session(engine) = Session(engine)


async def create_billboard(billboard: dict):
    with session:
        billboard: Billboard = Billboard(
            width=billboard["width"],
            height=billboard["height"],
            sides=billboard["sides"],
            surface=billboard["surface"],
            address=billboard["address"],
            pricePerDay=billboard["pricePerDay"],
            # booking=billboard["booking"]
        )
        session.add(billboard)
        session.commit()


async def get_billboard(billboard_id: str):
    billboard: Billboard = session.query(Billboard).filter(Billboard.id == billboard_id).scalar()
    return billboard

