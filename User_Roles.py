from sqlalchemy.orm import backref, relationship
from db_config import Base
from sqlalchemy import Column, BigInteger, String


class User_Roles(Base):
    __tablename__ = 'user_roles'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    role_name = Column(String(), unique=True)

    users = relationship("Users", backref=backref("user_roles", uselist=True))


