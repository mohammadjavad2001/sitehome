from pydantic import BaseModel,Field
from typing import Optional
from datetime import date
class User(BaseModel):
    id: int
    username: str 
    password: str
    phone: str
    isstaff: bool = False
    isactivate: bool = True
    class Config:
        orm_mode = True
class UserUpdate(BaseModel):
    username: str
    password:str
    phone:int
    isactivate:bool =True
    class Config:
        orm_mode=True



class AdvertisingBase(BaseModel):
    id: int
    user : int
    address: str
    city:str
    subject:str
    description: str
    price:int
    phone: str
    date:date
    is_active: bool = True    
    class Config:
        orm_mode = True    
