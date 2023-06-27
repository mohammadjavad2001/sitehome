from sqlalchemy.orm import Session

from . import user as table
from schemas import user as User
def create_user(db: Session, user: User.User):
    db_user = table.User(id=user.id,username = user.username,password=user.password,phone = user.phone,isactive = user.isactivate)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

