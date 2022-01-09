from db_config import Base
from sqlalchemy import Column, BigInteger, String, ForeignKey


class Administrators(Base):
    __tablename__ = 'administrators'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(String())
    last_name = Column(String())
    user_id = Column(BigInteger(), ForeignKey('users.id'), unique=True)