from db_config import Base
from sqlalchemy import Column, BigInteger, ForeignKey, UniqueConstraint


class Tickets(Base):
    __tablename__ = 'tickets'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    flight_id = Column(BigInteger(), ForeignKey('flights.id'))
    customer_id = Column(BigInteger(), ForeignKey('customers.id'))
    __table_args__ = (UniqueConstraint('flight_id', 'customer_id', name='_flight_customer_uc'), )
