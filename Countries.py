from sqlalchemy.orm import relationship, backref
from db_config import Base
from sqlalchemy import Column, String, Integer, LargeBinary


class Countries(Base):
    __tablename__ = 'countries'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(), unique=True)
    flag = Column(LargeBinary())

    incoming_flights = relationship("Flights", backref=backref("countries", uselist=True))
    outgoing_flights = relationship("Flights", backref=backref("countries", uselist=True))
    airline_companies = relationship("Airline_Companies", backref=backref("countries", uselist=True))