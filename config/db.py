from sqlalchemy import create_engine,MetaData
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base,DeclarativeMeta

password=os.getenv("MYSQL_ROOT_PASSWORD")

print(password,"   dewdweqqqaa")

engine = create_engine(f'mysql+pymysql://user:12345789!6mJb@10.96.5.8:3307/HELLOMY')   

meta = MetaData()

SessionLocal = sessionmaker(bind=engine)
conn = engine.connect()

print("DOWWWWWWWWWWWWWNNNNNNNNNNNNNNNNNNNNNNNNN123587146789641000")
