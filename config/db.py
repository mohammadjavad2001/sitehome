from sqlalchemy import create_engine,MetaData
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base,DeclarativeMeta

os.getenv("password")

engine = create_engine('mysql+pymysql://root:12345!6mJb@localhost:3306/HELLOMY')   
meta = MetaData()

SessionLocal = sessionmaker(bind=engine)
conn = engine.connect()
print("DOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNNNNNNNNNNNNNNNNNNNNNNNNN")
