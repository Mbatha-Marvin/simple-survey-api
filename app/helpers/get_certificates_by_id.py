from sqlalchemy import select
from app.core.db import engine
from sqlalchemy.orm import Session
from app.database.schemas import UserSchema


def get_certificates(user_id: int):
    with Session(engine) as session:
        stmt = select(UserSchema).where(UserSchema.id == user_id)
        user_details = session.scalars(statement=stmt).first()
        user_certificates = user_details.certificates

    return user_certificates
