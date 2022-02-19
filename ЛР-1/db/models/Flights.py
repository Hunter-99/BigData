from sqlalchemy import Column, Integer, Sequence, String, Float, TIMESTAMP
from db.base import Base


class Flights(Base):  # type: ignore
    supports_statement_cache = True
    __tablename__ = "flights"

    index = Column(Integer, Sequence("flights_id_sequence"), primary_key=True)
    year = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)
    day = Column(Integer, nullable=True)
    dep_time = Column(Float, nullable=True)
    sched_dep_time = Column(Integer, nullable=True)
    dep_delay = Column(Float, nullable=True)
    arr_time = Column(Float, nullable=True)
    sched_arr_time = Column(Integer, nullable=True)
    arr_delay = Column(Float, nullable=True)
    carrier = Column(String, nullable=True)
    flight = Column(Integer, nullable=True)
    tailnum = Column(String, nullable=True)
    origin = Column(String, nullable=True)
    dest = Column(String, nullable=True)
    air_time = Column(Float, nullable=True)
    distance = Column(Integer, nullable=True)
    hour = Column(Integer, nullable=True)
    minute = Column(Integer, nullable=True)
    time_hour = Column(TIMESTAMP, nullable=True)
