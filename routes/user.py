from fastapi import APIRouter,Depends, HTTPException,Path
from config.db import conn,SessionLocal
#from models.user import users
from sqlalchemy.orm import Session
from schemas.user import User,UserUpdate,AdvertisingBase
from sqlalchemy import exc
from typing import List
from cryptography.fernet import Fernet
from models import crud
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#@user.get("/users")
#def get_users():
#    return conn.execute(users.select()).fetchall()


Key= Fernet.generate_key()
f = Fernet(Key)

#@user.post("/usersbytable")
#def create_user(user: User):
#    print(user)
#    new_user = {"id":user.id,"username":user.username,"password":user.password,"phone":user.phone,"isactive":user.isactivate}
#   # new_user["password"] = f.encrypt(user.password.encode("utf-8"))
#    db:Session=Depends(get_db)
#
#    try:
#        result = conn.execute(users.insert().values(new_user))
#    except exc.SQLAlchemyError as e:
#        print(e)    
#
#    print(result)
#
#    return "user created"
#


#@user.get("/staticinserttable/")
#def hi():
#    new_user=new_user = {"id":912454,"username":"JOHEDN","password":"JFEFJEJFN5458","phone":888888,"isactive":False}
#    result = conn.execute(users.insert().values(new_user))
#    print(result)
   
@router.post("/users1/", response_model=User)
def create_user1(user: User, db: Session = Depends(get_db)):
       
    return crud.create_user(db=db, user=user)

@router.post("/advers1/", response_model=AdvertisingBase)
def create_advers1(advers: AdvertisingBase, db: Session = Depends(get_db)):
       
    return crud.create_advers(db=db, advers=advers)    


@router.get("/getallusers/",  response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        users = crud.get_users(db, skip=skip, limit=limit)

        return users

@router.get("/getadversby/{username}",  response_model=List[AdvertisingBase])
def get_advers1(username: str,skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
        advers = crud.get_adversbyuser(db,username=username ,skip=skip, limit=limit)

        return advers
#@app.post("/login/")
#async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
#    return {"username": username}
#    
@router.get("/specificusers1/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
            db_user = crud.get_user(db, user_id=user_id)

            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            
            return db_user

@router.put("/updateuser/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = crud.update_user(db,db_user=db_user,updateuser=user)
    return result  
      
@router.delete("/deleting/{user_id}",response_model=User)
def delete_user(user_id:int,db:Session = Depends(get_db)):
     db_user=crud.get_user(db,user_id=user_id)
     result = crud.delete_user(db,db_user)
     return result

