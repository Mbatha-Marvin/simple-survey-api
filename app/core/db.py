from sqlalchemy.orm import Session
from app.database.schemas import Base
from app.core.config import settings
from sqlalchemy import create_engine


engine = create_engine(settings.db_connection_string, echo=True)


def initialize_db():
    Base.metadata.create_all(bind=engine)


def get_db_session():
    with Session(engine) as session:
        yield session
