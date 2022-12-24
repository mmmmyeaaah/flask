import atexit

from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, func
from config import PG_DSN


engine = create_engine(PG_DSN)
Base = declarative_base(bind=engine)


class UserModel(Base):

    __tablename__ = 'app_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    adv = relationship('AdvertisementModel', backref='user')


class AdvertisementModel(Base):

    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('app_users.id'))


Base.metadata.create_all()

Session = sessionmaker(bind=engine)

atexit.register(lambda: engine.dispose())
