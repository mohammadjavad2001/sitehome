import os
import random
import shutil
from fastapi import APIRouter,Depends, File, HTTPException,Path, Request, UploadFile,status,Response
from pydantic import BaseModel, EmailStr
from config.db import conn,SessionLocal
#from models.user import users
from schemas.user import conf
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, MessageType
from cachetools import TTLCache,LRUCache

from sqlalchemy.orm import Session
from schemas.user import EmailSchema, User,UserUpdate,AdvertisingBase,Userreg
from sqlalchemy import exc
from typing_extensions import Annotated
from typing import List, Union
from cryptography.fernet import Fernet
from models import crud
import json
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Key= Fernet.generate_key()
f = Fernet(Key)

#@user.get("/users")
#def get_users():
#    return conn.execute(users.select()).fetchall()



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
   


#@router.post("/users/{user_id}/profile_picture")
#async def upload_profile_picture(user_id: int, file: UploadFile = File(...),db:Session=Depends(get_db)):
#    db_user=crud.get_user(db=db,user_id=user_id)
#    
#    if not db_user:
#        return {"error": "User not found"}
#
#    image_data = await file.read()  # Read binary image data from file upload
#      # Update user profile picture in database
#    return crud.upload_image(db=db,db_user=db_user,ima=image_data)   

cached_code=0
@router.post("/users1/",status_code=status.HTTP_200_OK)
async def create_user1(user:Userreg,response: Response,db:Session = Depends(get_db)):
    token_data = {
         "id" 
    }
    
    if(user.password==user.password_confirm):
        response.status_code = 201
        list_email=[user.email]
        
        crud.create_user(db=db, user=user)
    else:
        response.status_code = 400
# Create a cache with a time-to-live of 5 minutes
    user_id1=user.id
    cache_list=create_cache(user_id=user_id1)
    print(cache_list,"DEDDDDDDDDDDD")
    # Retrieve a verification code for a user
    if user.id in cache_list:
        
        code_check = cache_list[user_id1]
        cached_code1=code_check
        await send_code(user_email=list_email,cached_code=cached_code1)
        response.status_code=201
        print(code_check,"dwdwdffrf")
        #await post_code()
        return {"verify your email to activate your account",code_check}

    else:
        response.status_code=404
        return "code is not available"


class VerifyCodeRequest(BaseModel):
     verify_code : int
@router.post("/verifycode/{user_id}/",status_code=status.HTTP_201_CREATED)
async def post_code(user_id: int,request: VerifyCodeRequest,response: Response,db:Session = Depends(get_db)):
        if(cached_code==request.verify_code):
            crud.update_isactive(db=db,user_id=user_id)
            

             
            response.status_code=202
        return "Account activated"

@router.post("/email")
async def send_code(user_email:List[EmailStr],cached_code:int) -> JSONResponse:
    dest_email=user_email
    text=str(cached_code)
    print("sending email")
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> code is : """+text

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=user_email,
        body=html,
        subtype=MessageType.html)
        
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


def create_cache(user_id:int):
    cache1 = TTLCache(maxsize=100, ttl=300)
    code = random.randint(10000,99999)
    cache1[user_id] = code
    return cache1    

@router.post("/advers1/", response_model=AdvertisingBase)
def create_advers1(advers: AdvertisingBase, db: Session = Depends(get_db)):
       
    return crud.create_advers(db=db, advers=advers)    



@router.post("/profile_picture/{user_id}/")
async def upload_profile_picture(user_id: int, file: UploadFile = File(...),db:Session=Depends(get_db)):
    upload_dir = os.path.join(os.getcwd(), "uploads")
    db_user=crud.get_user(db=db,user_id=user_id)

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # get the destination path
    dest = os.path.join(upload_dir, file.filename)
    # copy the file contents
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)    
    
    return crud.upload_image(db=db,db_user=db_user,image=dest)

@router.post("/advers1/", response_model=AdvertisingBase)
def create_advers1(advers: AdvertisingBase, db: Session = Depends(get_db)):
       
    return crud.create_advers(db=db, advers=advers)    


@router.get("/getallusers/",response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        users = crud.get_users(db, skip=skip, limit=limit)

        return users

@router.get("/getadversby/{username}",  response_model=List[AdvertisingBase])
def get_advers1(username: str,skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
        advers = crud.get_adversbyuser(db,username=username ,skip=skip, limit=limit)

        return advers

    
@router.get("/specificusers1/{user_id}",response_model_exclude_unset=True)
def read_user(user_id: int, db: Session = Depends(get_db)):
            db_user = crud.get_user(db, user_id=user_id)

            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            
            return db_user

@router.put("/updateuser/{user_id}", response_model=User,response_model_exclude_unset=True)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = crud.update_user(db,db_user=db_user,updateuser=user)
    return result  
@router.patch("/isseller/{user_id}",response_model_exclude_unset=True)
def update_user2(user_id: int, db: Session = Depends(get_db)):
    user_c = crud.get_user(db, user_id=user_id)
    listadvers=get_advers1(username=user_c.username,db=db)
    if(len(listadvers)==0):
        return False
    else:
         crud.seller_True(db=db,db_user=user_c)

         return True
         

@router.delete("/deleting/{user_id}",response_model=User,response_model_exclude_unset=True)
def delete_user(user_id:int,db:Session = Depends(get_db)):
    db_user=crud.get_user(db,user_id=user_id)
    result = crud.delete_user(db,db_user)
    return result

