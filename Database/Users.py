from sqlalchemy.orm import relationship, backref

from db_config import Base
from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, LargeBinary


class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    username = Column(String(), unique=True)
    password = Column(String())
    email = Column(String(), unique=True)
    user_role = Column(Integer(), ForeignKey('user_roles.id'))
    thumbnail = Column(LargeBinary(), nullable=True)

    airline_companies = relationship("Airline_Companies", backref=backref("users", uselist=True))
    administrators = relationship("Administrators", backref=backref("users", uselist=True))