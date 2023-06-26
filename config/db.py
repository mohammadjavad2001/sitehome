from sqlalchemy import create_engine,MetaData
engine = create_engine("mysql+mysqlconnector://root:12345!6mJb@localhost:3306/homes")
meta = MetaData()
conn = engine.connect()
