import hashlib
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import LargeBinary
from . import user as ormmodels
from schemas import user as pydantic_models


def create_user(db: Session, user: pydantic_models.User):
    hash_pass=hashlib.md5(user.password.encode('utf-8')).hexdigest()
    db_token = ormmodels.User(id=user.id,username = user.username,password=hash_pass,phone = user.phone,
                             isactive = user.isactivate,email=user.email)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def create_revoke_token(db: Session, token: pydantic_models.revoke_token):
    db_user = ormmodels.RevokedToken(id=token.id, token= token.token,user_id=token.user_id,
                                     revoked_at=token.revoked_at,is_expired=token.is_expired)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_advers(db: Session, advers: pydantic_models.AdvertisingBase):
    db_advers = ormmodels.Advers(id=advers.id,user = advers.user,address=advers.address,city = advers.city,
                                 subject = advers.subject,description=advers.description,price=advers.price,
                                 phone=advers.phone,date=advers.date,isactive=advers.is_active)
    db.add(db_advers)
    db.commit()
    db.refresh(db_advers)
    return db_advers

def get_adversbyuser(db: Session, username:str,skip: int = 0, limit: int = 100):
    
    user1=db.query(ormmodels.User).filter(ormmodels.User.username == username).first()
    user_id=user1.id
    adver=db.query(ormmodels.Advers).filter(ormmodels.Advers.user==user_id).all()
    return adver

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ormmodels.User).all()

def get_user(db: Session, user_id: int):
    return db.query(ormmodels.User).filter(ormmodels.User.id == user_id).first()

def get_userbyusername(db: Session, username: str):
    return db.query(ormmodels.User).filter(ormmodels.User.username == username).first()

def update_user(db: Session,db_user:pydantic_models.User,updateuser:pydantic_models.UserUpdate):
    update_data = updateuser.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def update_advers(db: Session,db_advers:pydantic_models.AdvertisingBase,updateadvers:pydantic_models.Adversupdate):
    update_data = updateadvers.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_advers, key, value)
    db.add(db_advers)
    db.commit()
    db.refresh(db_advers)
    return db_advers
def seller_True(db: Session,db_user:pydantic_models.User):
    db_user.is_seller=True      
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_advers(db:Session,advers_id:int):
    return db.query(ormmodels.Advers).filter(ormmodels.Advers.id==advers_id).first()



def upload_image(db:Session,db_user:pydantic_models.User,image:str):
    db_user.profile_picture=image
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session,db_user:pydantic_models):
    db.delete(db_user)
    db.commit()
    return db_user

def update_isactive(db: Session,user_id:int):
    db_user=get_user(db=db,user_id=user_id)
    db_user.isactive=True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
