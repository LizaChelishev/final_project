from sqlalchemy.orm import relationship, backref
from db_config import Base
from sqlalchemy import  Column, BigInteger,  String, ForeignKey


class Customers(Base):
    __tablename__ = 'customers'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(String())
    last_name = Column(String())
    address = Column(String())
    phone_no = Column(String(), unique=True)
    credit_card_no = Column(String(), unique=True)
    user_id = Column(BigInteger(), ForeignKey('users.id'), unique=True)

    tickets = relationship("Tickets", backref=backref("customers", uselist=True))
    user = relationship("Users", backref=backref("customers", uselist=False))
