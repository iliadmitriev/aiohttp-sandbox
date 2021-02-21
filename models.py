from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    MetaData
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

metadata = MetaData()


class Profile(Base):
    __tablename__ = 'profile'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    firstname = Column('firstname', String(100))
    surname = Column('surname', String(100))
    user_id = Column('user_id', Integer, index=True, unique=True)
    birthdate = Column('birthdate', Date)
    gender = Column('gender', String(10))
    avatar = Column('avatar', String(200))

    def __repr__(self):
        return f'{self.id}: {self.firstname} {self.surname}'


class Config(Base):
    __tablename__ = 'config'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, index=True, unique=True)
    language = Column('language', String(5))
    dark_mode = Column('dark_mode', Boolean)


