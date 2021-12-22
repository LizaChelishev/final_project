from db_config import Base
from sqlalchemy import Column, String, Integer, LargeBinary


class Countries(Base):
    __tablename__ = 'countries'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(), unique=True)
    flag = Column(LargeBinary())