from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import DB_URL

engine = create_engine(url=DB_URL, echo=False)

class Base(DeclarativeBase):
    pass

session_factory = sessionmaker(engine)

def get_session():
    with session_factory() as session:
        yield session
