from sqlalchemy import Table,Date, Boolean, Column, ForeignKey, Integer, String
from config.db import meta,engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base,DeclarativeMeta

SessionLocal = sessionmaker()
Base = declarative_base()
#users = Table(
#    'users',meta,
#    Column('id',Integer,primary_key=True),
#    Column('username',String(255)),
#    Column('password',String(255)),
#    Column('phone',Integer),
#    Column('isactive',Boolean),
#)
#adversting = Table(
#    'adversting',meta,
#    Column('id',Integer,primary_key=True),
#    Column('user_id', Integer, ForeignKey('users.id')),
#    Column('subject',String(255)),
#    Column('description',String(255)),
#    Column('phone',Integer),
#    Column('date',Date),
#    Column('isactive',Boolean),
#)
#
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    isstaff = Column(Boolean,default=False)
    username = Column(String(255), index=True)
    password = Column(String(255))
    phone = Column(String(255), index=True)
    isactive = Column(Boolean, default=True)


class Advers(Base):
    __tablename__ = "adversting"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey('users.id'))
    address = Column(String(255))
    city = Column(String(255))
    subject = Column(String(255),index=True)
    description = Column(String(255))
    phone = Column(String(255), index=True)
    price = Column(Integer)
    date = Column(Date)
    isactive = Column(Boolean,default=True)

Base.metadata.create_all(engine)