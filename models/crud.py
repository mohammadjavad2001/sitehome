from sqlalchemy.orm import Session

from . import user as ormmodels
from schemas import user as User
def create_user(db: Session, user: User.User):
    db_user = ormmodels.User(id=user.id,username = user.username,password=user.password,phone = user.phone,isactive = user.isactivate)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ormmodels.User).all()

def get_user(db: Session, user_id: int):
    return db.query(ormmodels.User).filter(ormmodels.User.id == user_id).first()

def update_user(db: Session,db_user:User.User,updateuser:User.UserUpdate):
    update_data = updateuser.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def delete_user(db:Session,db_user:User):
    db.delete(db_user)
    db.commit()
    return db_user