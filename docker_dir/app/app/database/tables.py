from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey

from app.database.engine import Base

class ColorsTable(Base):
    __tablename__ = 'colors'

    id: Mapped[int] =  mapped_column(primary_key= True)
    color: Mapped[str] = mapped_column(nullable=False) 


class BreedsTable(Base):
    __tablename__ = 'breeds'

    id: Mapped[int] =  mapped_column(primary_key= True)
    breed: Mapped[str] = mapped_column(nullable=False)


class KittensTable(Base):
    __tablename__ = 'kittens'

    id: Mapped[int] =  mapped_column(primary_key= True)
    name: Mapped[str] = mapped_column(nullable=False) 
    age: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str]
    color_id: Mapped[int] = mapped_column(ForeignKey('colors.id',ondelete='RESTRICT', onupdate='CASCADE'))
    breed_id: Mapped[str] = mapped_column(ForeignKey('breeds.id',ondelete='RESTRICT', onupdate='CASCADE'))
    