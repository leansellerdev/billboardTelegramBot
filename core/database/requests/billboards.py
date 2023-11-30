import os

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from core.database.models.db_models import Billboard

from core.database.requests.staff import basedir

engine = create_engine(f"sqlite:///{os.path.join(basedir, 'database.db')}", echo=True)
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


async def get_billboard_by_id(billboard_id: str):
    with session:
        billboard: Billboard = session.query(Billboard).filter(Billboard.id == billboard_id).scalar()

    return billboard


async def get_billboard_by_name(billboard_name: str):
    with session:
        billboard: Billboard = session.query(Billboard).filter(Billboard.name == billboard_name).scalar()

    return billboard


async def change_price(billboard_name: str, new_price: str):

    with session:
        billboard = session.scalar(select(Billboard).filter_by(name=billboard_name))
        billboard.pricePerDay = float(new_price)

        session.commit()
