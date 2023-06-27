from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String
from config.db import meta,engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SessionLocal = sessionmaker()
Base = declarative_base()
users = Table(
    'users',meta,
    Column('id',Integer,primary_key=True),
    Column('username',String(255)),
    Column('password',String(255)),
    Column('phone',Integer),
    Column('isactive',Boolean),
)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    phone = Column(Integer, index=True)

    isactive = Column(Boolean, default=True)
meta.create_all(engine)