from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, String, SmallInteger, Float
from sqlalchemy.orm import mapped_column

from api.entity.base import Base


class Movie(Base):
    __tablename__ = "movie"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String, nullable=False)
    genres = mapped_column(String)
    year = mapped_column(SmallInteger)
    view = mapped_column(Integer)
    rating = mapped_column(Float)
    embedding = mapped_column(Vector(768))
