from sqlalchemy import create_engine,MetaData
engine = create_engine("mysql+mysqlconnector://root:12345!6mJb@localhost:3306/HELLO")
meta = MetaData()
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(bind=engine)

conn = engine.connect()
