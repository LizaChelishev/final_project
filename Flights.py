from db_config import Base
from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey


class Flights(Base):
    __tablename__ = 'flights'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger(), ForeignKey('airline_companies.id'))
    origin_country_id = Column(Integer(), ForeignKey('countries.id'))
    destination_country_id = Column(Integer(), ForeignKey('countries.id'))
    departure_time = Column(DateTime())
    landing_time = Column(DateTime())
    remaining_tickets = Column(Integer())
