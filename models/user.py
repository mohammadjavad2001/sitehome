from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String
from config.db import meta,engine
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker()

users = Table(
    'users',meta,
    Column('id',Integer,primary_key=True),
    Column('username',String(255)),
    Column('password',String(255)),
    Column('phone',Integer),
    Column('isactive',Boolean),
)
meta.create_all(engine)