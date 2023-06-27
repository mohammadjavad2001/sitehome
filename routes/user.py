from fastapi import APIRouter,Depends
from config.db import conn,SessionLocal
from models.user import users
from sqlalchemy.orm import Session
from schemas.user import User
from cryptography.fernet import Fernet
from models.crud import create_user as create
user = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@user.get("/users")
def get_users():
    return conn.execute(users.select()).fetchall()
Key= Fernet.generate_key()
f = Fernet(Key)

@user.post("/users")
def create_user(user: User):
    print(user)
    new_user = {"id":user.id,"username":user.username,"phone":user.phone,"isactive":user.isactivate}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    print(result)
    return "user created"

@user.post("/users1/", response_model=User)
def create_user1(user: User, db: Session = Depends(get_db)):
   
    return create(db=db, user=user)
    'users',meta,
    Column('id',Integer,primary_key=True),
    Column('username',String(255)),
    Column('password',String(255)),
    Column('phone',Integer),
    Column('isactive',Boolean),
