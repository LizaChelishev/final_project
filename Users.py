from db_config import Base
from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey


class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    username = Column(String(), unique=True)
    password = Column(String())
    email = Column(String(), unique=True)
    user_role = Column(Integer(), ForeignKey('user_roles.id'))
