from sqlalchemy.orm import relationship, backref
from db_config import Base
from sqlalchemy import Column, BigInteger, String, ForeignKey


class Administrators(Base):
    __tablename__ = 'administrators'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(String())
    last_name = Column(String())
    user_id = Column(BigInteger(), ForeignKey('users.id'), unique=True)

    user = relationship('User', backref=backref("administrators", uselist=False, passive_deletes=True))

    def __repr__(self):
        return f'Administrator(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, ' \
               f'user_id={self.user_id})'

    def __str__(self):
        return f'Administrator[id={self.id}, first_name={self.first_name}, last_name={self.last_name}, ' \
               f'user_id={self.user_id}]'