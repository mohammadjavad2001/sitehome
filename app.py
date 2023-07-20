from fastapi import FastAPI
app = FastAPI()
#from routes.user import app
#app.include_router(app)
from datetime import datetime as DT
from datetime import timedelta
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

import redis

from sqlalchemy.orm import Session
from schemas.user import EmailSchema, User,UserUpdate,AdvertisingBase,Userreg,LoginUser,Adversupdate
from sqlalchemy import exc
from typing_extensions import Annotated
from typing import Any, List, Union
from cryptography.fernet import Fernet
from models import crud
from opentelemetry import trace    

import json
otel_trace: Any = os.environ.get("OTELE_TRACE")
print(otel_trace)
if otel_trace == "true": 
 #   from opentelemetry import trace
 #   from opentelemetry.trace import SpanKind
 #   from opentelemetry.sdk.trace import TracerProvider
 #   from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
 #   from opentelemetry.sdk.trace.export import BatchSpanProcessor
 #   from opentelemetry.sdk.resources import Resource
#
 #   resource = Resource(attributes={
 #       "service.name": "my_service1"
 #   })
#
 #   trace.set_tracer_provider(TracerProvider(resource=resource))
#
 #   otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
#
#
 #   trace.get_tracer_provider().add_span_processor(
 #       BatchSpanProcessor(otlp_exporter)
 #   )
#
 #   tracer = trace.get_tracer(__name__)
#
 #   with tracer.start_as_current_span("foo", kind=SpanKind.SERVER):
 #       with tracer.start_as_current_span("bar", kind=SpanKind.SERVER):
 #           with tracer.start_as_current_span("baz", kind=SpanKind.SERVER):
 #               print("Hello world from OpenTelemetry Python!")
    from opentelemetry import trace
    from opentelemetry.exporter.jaeger import thrift
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    #from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (OTLPSpanExporter,)
    # from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

    trace.set_tracer_provider(TracerProvider(resource=Resource.create(attributes={"service.name": "my_service","service_name":"fasttt"}))) 
    trace_exporter = thrift.JaegerExporter(
         agent_host_name="172.28.5.11",
         agent_port=6831)
    tracer = trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(trace_exporter))
    FastAPIInstrumentor.instrument_app(app)
    from config.db import engine
    dbinstrumentor = SQLAlchemyInstrumentor()
    dbinstrumentor.instrument(engine=engine)
    print("jaeger connected to fastapi")
else:
        pass
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
import elasticapm.instrumentation.control as instr
apm_config = {
'SERVICE_NAME': 'DemoFastAPI',
'DEBUG': True,
'SERVER_URL': 'http://172.28.5.20:8200',
'CAPTURE_HEADERS': True,
'ENVIRONMENT': 'dev',
'CAPTURE_BODY': 'all',
'GLOBAL_LABELS': 'platform=DemoPlatform, application=DemoApplication',
'SECRET_TOKEN': 'cacc7099dcedff3ac82b0f225533f81439871f5952f39f555f02fc45a2bfa12c'
}
#
apm = make_apm_client(apm_config)
#
#apm = make_apm_client(apm_config)
##apm = ElasticAPM(app=app,client=apm,service_name="my-fastapi-app", secret_token="cacc7099dcedff3ac82b0f225533f81439871f5952f39f555f02fc45a2bfa12c",service_url="http://172.28.5.20:9200")
##app.add_middleware(ElasticAPM, client=apm)
server_url = 'http://172.28.5.20:8200'
service_name = 'DemoFlask'
environment = 'dev'
#apm = ElasticAPM(app, server_url=server_url, 
#      service_name=service_name, environment=environment,client =)

app.add_middleware(ElasticAPM, client=apm)
print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
    
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
# 
#   

#@router.on_event("startup")
#async def startup():
#    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#
#    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#    print("gfregfrg")
#
redis_client = redis.Redis(host='rediscache', port=6379, db=0)

async def coderedis_cache(user_id:int):
      code_cache=random.randint(10000,99999)
      redis_client.setex(name=str(user_id),time=300,value=code_cache)
      return code_cache

@app.post("/email/{user_id}/")
async def send_code(user_id:int,db:Session = Depends(get_db)) -> JSONResponse:
    user=crud.get_user(db=db,user_id=user_id)
    code = await coderedis_cache(user_id=user_id)
    print(user.email)
    print("sending email")
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> code is : """+str(code)
    print(html)
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[user.email],
        body=html,
        subtype=MessageType.html) 
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

class VerifyCodeRequest(BaseModel):
     verify_code : int     
@app.post("/verifycode/{user_id}/",status_code=status.HTTP_201_CREATED)
async def post_code(user_id: int,request: VerifyCodeRequest,response: Response,db:Session = Depends(get_db)):
        
        if(str(redis_client.get(name=user_id))[2:7]==str(request.verify_code)):
           
            crud.update_isactive(db=db,user_id=user_id)
            response.status_code=202
            return "Account activated"
        else:
             response.status_code=404
             return "Code is not correct"






@app.post("/users1/",status_code=status.HTTP_200_OK)
async def create_user1(user:Userreg,response: Response,db:Session = Depends(get_db)):
    
    if(user.password==user.password_confirm):
        response.status_code = 201
        list_email=[user.email]
        
        return crud.create_user(db=db, user=user)
    else:
        response.status_code = 400
        return response.status_code 
# Create a cache with a time-to-live of 5 minutes

    # Retrieve a verification code for a user



#class VerifyCodeRequest(BaseModel):
#     verify_code : int
#@router.post("/verifycode/{user_id}/",status_code=status.HTTP_201_CREATED)
#async def post_code(user_id: int,request: VerifyCodeRequest,response: Response,db:Session = Depends(get_db)):
#        if(==request.verify_code):
#            crud.update_isactive(db=db,user_id=user_id)
#            
#
#            print("dode corrrect ") 
#            response.status_code=202
#        return "Account activated"


@app.post("/advers1/", response_model=AdvertisingBase)
def create_advers1(advers: AdvertisingBase, db: Session = Depends(get_db)):
       
    return crud.create_advers(db=db, advers=advers)    



@app.post("/profile_picture/{user_id}/")
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

@app.post("/advers1/", response_model=AdvertisingBase)
def create_advers1(advers: AdvertisingBase, db: Session = Depends(get_db)):
       
    return crud.create_advers(db=db, advers=advers)    


@app.get("/getallusers/",response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        users = crud.get_users(db, skip=skip, limit=limit)

        return users

@app.get("/getadversby/{username}",  response_model=List[AdvertisingBase])
def get_advers1(username: str,skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
        advers = crud.get_adversbyuser(db,username=username ,skip=skip, limit=limit)

        return advers

    
@app.get("/specificusers1/{user_id}",response_model_exclude_unset=True)
def read_user(user_id: int, db: Session = Depends(get_db)):
            db_user = crud.get_user(db, user_id=user_id)

            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            
            return db_user

@app.put("/updateuser/{user_id}", response_model=User,response_model_exclude_unset=True)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = crud.update_user(db,db_advers=db_user,updateuser=user)
    return result  


@app.patch("/isseller/{user_id}",response_model_exclude_unset=True)
def update_user2(user_id: int, db: Session = Depends(get_db)):
    user_c = crud.get_user(db, user_id=user_id)
    listadvers=get_advers1(username=user_c.username,db=db)
    if(len(listadvers)==0):
        return False
    else:
         crud.seller_True(db=db,db_user=user_c)

         return True
         

@app.delete("/deleting/{user_id}",response_model=User,response_model_exclude_unset=True)
def delete_user(user_id:int,db:Session = Depends(get_db)):
    db_user=crud.get_user(db,user_id=user_id)
    result = crud.delete_user(db,db_user)
    return result

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import hashlib
from jose import JWTError, jwt
SECRET_KEY = "cacc7099dcedff3ac82b0f225533f81439871f5952f39f555f02fc45a2bfa12c"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token",scheme_name="User")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = DT.now() + expires_delta
    else:
        expire = DT.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt    

@app.post("/checktokenOK/")
def get_current_user(token: Annotated[str,Depends(oauth2_scheme)],db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("sdvfsdv")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print("DSV")
        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    user = crud.get_userbyusername(db=db, username=username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/adversupdate/{advers_id}", response_model=AdvertisingBase)
def update_advers(advers_id:int,token:Annotated[str,Depends(oauth2_scheme)],advers_update:Adversupdate,db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:    
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        user_id=crud.get_userbyusername(db=db,username=username).id
        advers1_id=crud.get_advers(db=db,advers_id=advers_id).user
        if(advers1_id==user_id):
             advers1=crud.get_advers(db=db,advers_id=advers_id)                                         
             crud.update_user(db=db,db_advers=advers1,updateadvers=advers_update)
             return status.HTTP_202_ACCEPTED
        else:
             raise credentials_exception
    except JWTError:
        raise credentials_exception

def Authenticate(form_data: LoginUser,db:Session = Depends(get_db)):
    db_user = crud.get_userbyusername(db=db,username=form_data.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    
    hashed_password = hash_pass=hashlib.md5(form_data.password.encode('utf-8')).hexdigest()
    if not hashed_password == db_user.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return db_user





@app.post("/token" ,response_model=Token)
async def login_for_access_token(
    form_data: LoginUser,db:Session = Depends(get_db)):

    user = Authenticate(db=db, form_data=form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if (user.isactive==True):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
         raise HTTPException(
              status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
              detail="User is not Active please verify your email"
         )
