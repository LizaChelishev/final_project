from sqlalchemy.orm import relationship, backref
from db_config import Base
from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey


class Airline_Companies(Base):
    __tablename__ = 'airline_companies'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(String(), unique=True)
    country_id = Column(Integer(), ForeignKey('countries.id'))
    user_id = Column(BigInteger(), ForeignKey('users.id'), unique=True)

    flights = relationship("Flights", backref=backref("airline_companies", uselist=True))


