from sqlalchemy import URL, Table,Date,DateTime, Boolean, Column, ForeignKey, Integer, String,LargeBinary
from config.db import meta,engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base,DeclarativeMeta

SessionLocal = sessionmaker()
Base = declarative_base()
class RevokedToken(Base):
    __tablename__ = "revoked_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(256), unique=True, index=True)
    user_id = Column(Integer)
    revoked_at = Column(DateTime)
    is_expired = Column(Boolean, default=False)
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    isstaff = Column(Boolean,default=False)
    username = Column(String(255), index=True,unique=True)
    password = Column(String(255))
    phone = Column(String(255), index=True)
    isactive = Column(Boolean, default=False)
    email =Column(String(255))
    profile_picture = Column(String(512), nullable=True)
    is_seller = Column(Boolean,default=False)
    
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