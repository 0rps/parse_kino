from sqlalchemy import Table, Column, Integer, Unicode, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from baseapp.db import Base
# engine = create_engine('postgresql+psycopg2://orps:pass1234@localhost/afishadb')


class Cinema(Base):

    __tablename__ = 'cinema'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(128), nullable=False)
    address = Column(Unicode(128), nullable=False)
    metro = Column(Unicode(128), nullable=True)
    rating = Column(Float, nullable=True)
    votes = Column(Integer, default=0)

    showtimes = relationship("Showtime")


class Movie(Base):

    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(256), nullable=False)
    info = Column(Unicode(512), nullable=True)
    rating = Column(Float, nullable=True)
    votes = Column(Integer, nullable=True)

    showtimes = relationship("Showtime")


class Showtime(Base):

    __tablename__ = 'showtime'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer, ForeignKey('cinema.id'))
    movie_id = Column(Integer, ForeignKey('movie.id'))

    dt = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)



# Create your models here.
