from pydantic import BaseModel, EmailStr,Field,validator
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from typing import List, Optional
from datetime import date
class User(BaseModel):
    id: int
    username: str 
    password: str
    phone: str
    email: EmailStr
    isstaff: bool = False
    isactivate: bool = False
    is_seller:bool=False
    
    profile_picture:Optional[str]=None     
   
    class Config:
        orm_mode = True
class UserUpdate(BaseModel):
    username: str
    email:EmailStr
    phone:int
    isactivate:bool =True
    is_seller : bool=False
    class Config:
        orm_mode=True
class Userreg(User):
    password_confirm : str

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
class EmailSchema(BaseModel):
   email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = "mohammadj20012121@gmail.com",
    
    MAIL_PASSWORD = "bpwmdcwkqimwjuox",
    MAIL_FROM = "mohammadj20012121@yahoo.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True
)   