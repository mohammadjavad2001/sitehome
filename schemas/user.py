from pydantic import BaseModel,Field
from typing import Optional
from datetime import date

class User(BaseModel):
    id: Optional[int]
    username: str 
    password: str
    phone: int
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
    user_id : int = Field(foreign_key="user.id")
    address: str
    price:int
    phone: str
    date:date
    is_active: bool     
    class Config:
        orm_mode = True    
