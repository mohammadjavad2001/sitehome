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
from schemas.user import revoke_token,EmailSchema, User,UserUpdate,AdvertisingBase,Userreg,LoginUser,Adversupdate
from sqlalchemy import exc
from typing_extensions import Annotated
from typing import Any, List, Union
from cryptography.fernet import Fernet
from models import crud
from opentelemetry import trace    

#Jaeger
import json
otel_trace: Any = os.environ.get("OTELE_TRACE")
print(otel_trace)
if otel_trace == "true": 
 #  from opentelemetry import trace
 #  from opentelemetry.trace import SpanKind
 #  from opentelemetry.sdk.trace import TracerProvider
 #  from opentelemetry.exporter.jaeger.thrift import JaegerExporter
 #  from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
 #  from opentelemetry.sdk.trace.export import BatchSpanProcessor
 #  from opentelemetry.sdk.resources import Resource
 #  resource = Resource(attributes={
 #      "service.name": "my_service1"
 #  })
#
 #  trace.set_tracer_provider(TracerProvider(resource=resource))
 #  otlp_exporter = OTLPSpanExporter(endpoint="http://172.28.5.11:14250", insecure=True)
 #  trace.get_tracer_provider().add_span_processor(
 #      BatchSpanProcessor(otlp_exporter)
 #  )
 #  tracer = trace.get_tracer(__name__)
 #  with tracer.start_as_current_span("foo", kind=SpanKind.SERVER):
 #      with tracer.start_as_current_span("bar", kind=SpanKind.SERVER):
 #          with tracer.start_as_current_span("baz", kind=SpanKind.SERVER):
 #              print("Hello world from OpenTelemetry Python!").
 #   
 #  resource = Resource(attributes={
 #      "service.name": "wwdwwd"
 #  })
 #  
 #  jaeger_exporter = JaegerExporter(
 #      agent_host_name="172.28.5.11",
 #      agent_port=6831,
 #  )
 #  
 #  provider = TracerProvider(resource=resource)
 #  processor = BatchSpanProcessor(jaeger_exporter)
 #  provider.add_span_processor(processor)
 #  trace.set_tracer_provider(provider)
 # 
   #from opentelemetry import metrics
   #from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
   #from opentelemetry.sdk.metrics import MeterProvider
   #from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
   #from opentelemetry.sdk.resources import SERVICE_NAME, Resource
   #resource = Resource(attributes={
   # SERVICE_NAME: "your-name"
   # })
   #reader = OTLPMetricExporter(endpoint="172.28.5.11:14269")
   # #     - "14268:14268"
   # 
   # #  - "14269:14269"
   # #  - "4317:4317"
   # #  - "4318:4318"
   # #  - "14250:14250"
   #provider = MeterProvider(resource=resource, metric_readers=[reader])
   #metrics.set_meter_provider(provider)
   from opentelemetry import trace
   from opentelemetry.exporter.jaeger import thrift
   from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
   from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
   from opentelemetry.sdk.resources import Resource
   from opentelemetry.sdk.trace import TracerProvider
   from opentelemetry.sdk.trace.export import BatchSpanProcessor
   #from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (OTLPSpanExporter,)
   # from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
   trace.set_tracer_provider(TracerProvider(resource=Resource.create(attributes={"service.name": "MONITORAPI","service_name":"fasttt"}))) 
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


#APM ELASTIC SEARCH
# from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
# import elasticapm.instrumentation.control as instr
# apm_config = {
#             'SERVICE_NAME': 'DemoFastAPI',
#             'DEBUG': True,
#             'SERVER_URL': 'http://172.28.5.20:8200',
#             'CAPTURE_HEADERS': True,
#             'ENVIRONMENT': 'dev',
#             'CAPTURE_BODY': 'all',
#             'GLOBAL_LABELS': 'platform=DemoPlatform, application=DemoApplication',
#             'SECRET_TOKEN': 'cacc7099dcedff3ac82b0f225533f81439871f5952f39f555f02fc45a2bfa12c'
#              }
# #
# apm = make_apm_client(apm_config)
# #
# #apm = make_apm_client(apm_config)
# ##apm = ElasticAPM(app=app,client=apm,service_name="my-fastapi-app", secret_token="cacc7099dcedff3ac82b0f225533f81439871f5952f39f555f02fc45a2bfa12c",service_url="http://172.28.5.20:9200")
# ##app.add_middleware(ElasticAPM, client=apm)
# server_url = 'http://172.28.5.20:8200'
# service_name = 'DemoFlask'
# environment = 'dev'
# #apm = ElasticAPM(app, server_url=server_url, 
# #      service_name=service_name, environment=environment,client =)

# app.add_middleware(ElasticAPM, client=apm)
# print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")






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
def read_users(db: Session = Depends(get_db)):
        skip= 0
        limit = 100
        users = crud.get_users(db=db, skip=skip, limit=limit)

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
    
    result = crud.update_user(db,db_user=db_user,updateuser=user)
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


from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import hashlib
from jose import JWTError, jwt
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi.responses import RedirectResponse

from fastapi_oidc import IDToken
from fastapi_oidc import get_auth
import requests
# OIDC_config = {
#    "client_id": "fastapi",
#    "base_authorization_server_uri": "http://0.0.0.0:8090/auth/realms/fast/protocol/openid-connect/auth",
#    "issuer": "http://localhost:8080/auth/realms/fast",
#    "signature_cache_ttl": 3600,
# }

# authenticate_user=get_auth(**OIDC_config)



# @app.get("/protected")
# def protected(id_token: IDToken = Depends(authenticate_user)):
#    return {"Hello": "World", "user_email": id_token.email}

# -----------------------------------------------------------------------------------
from keycloak import KeycloakOpenID

keycloak_openid = KeycloakOpenID(server_url="http://172.28.5.90:8080/auth/",
                                 client_id="fastapi",
                                 realm_name="fast",
                                 client_secret_key="qNnqdLpdZgPvpxXmknz3D65r5tIx5S8k",
                                 verify=False
                                )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token",scheme_name="User")
def get_current_user3(token: str):
    try:

        userinfo = keycloak_openid.userinfo(token)
        return [True,userinfo]
#     URL_TOKEN = "realms/{realm-name}/protocol/openid-connect/token"
# URL_USERINFO = "realms/{realm-name}/protocol/openid-connect/userinfo"
    except:
        return [False]

class datakeycloak(BaseModel):
    username: str
    password: str
    
@app.post("/loging")
def loging(data:datakeycloak):
    try:
        token=keycloak_openid.token(username=data.username,password=data.password)
        return f"successfully logged in {token}"
    except Exception:
        return Response(content="username or password invalid ",status_code=status.HTTP_404_NOT_FOUND)

@app.post("/loggout")
def loging(token: str = Depends(oauth2_scheme)):
    try:
        
        keycloak_openid.logout(refresh_token=token)
        return Response(content=f"successfully logged out",status_code=status.HTTP_200_OK)
    
    except Exception:
        return Response(content="you are not login ",status_code=status.HTTP_404_NOT_FOUND)

@app.get("/secure-resource")
async def secure_resource(token: str = Depends(oauth2_scheme)):
    response_auth=get_current_user3(token=token)
    if(response_auth[0]==True):

        return {"message": f"{response_auth[1]}"}
    else:
        return{"messsage":"token invalid"}

@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    
    response_auth=get_current_user3(token=token)
    
    if(response_auth[0]==True):

        return {"message": "DQWDWDQWD"}
    else:
        return{"messsage":"token invalid"}
    
@app.get("/login")
async def login():
   # Redirect to Keycloak login page
   
   return RedirectResponse(keycloak_openid.auth_url(redirect_uri="http://192.168.107.23:8080/callback"))
    #return RedirectResponse("http://192.168.107.23:8090/auth/realms/fast/protocol/openid-connect/auth?response_type=code&client_id=fastapi")
   
@app.get("/callback")
def callback(code: str):
    # try:
    #     url = "http://172.28.5.90:8080/auth/realms/fast/protocol/openid-connect/token"
    #     headers = {
    #                 'Content-Type': "application/x-www-form-urlencoded",
    #                 }
    #     print(headers)
    #     #data1 = "grant_type=password&username=admin&password=123&scope=apim:api_view apim:api_create"
    #     #print(f"{data1}")
    #     data = {
    #         "grant_type": "authorization_code",
    #         "code": f'{code}',
    #         "client_id": f'{keycloak_openid.client_id}',
    #         "client_secret": f'{keycloak_openid.client_secret_key}',
    #         "redirect_uri": "http://192.168.107.23:8080/callback"
    #         }
    #     response = requests.post(url=url, headers=headers, data=data, verify=False)  # Use verify=False to ignore SSL
        
    #     try:
    #         return Response(status_code=response.status_code,content=response.json())
    #     except Exception:
    #         return Response(content=response.content,status_code=response.status_code)
    # except Exception:
    #         return Response(data={"detail":"raised an Exception"}, status=status.HTTP_404_NOT_FOUND)  
#    token = keycloak_openid.token(code,"http://localhost:8080/callback")
    
    token = keycloak_openid.token(
        grant_type="authorization_code",
        code=code,
        redirect_uri="http://192.168.107.23:8080/callback"
        )
    
    access_token = token['access_token']
    refresh_token = token['refresh_token']
    return {f'detail": "Authentication successful! {token}'}   
   #-----------------------------------------------------------------

#- - - - - -- - - - -- - - - -- - - - -- - - - -- - ------------------------------------------------------------
# from fastapi_keycloak import FastAPIKeycloak, OIDCUser

# idp = FastAPIKeycloak(

#     server_url="http://0.0.0.0:8090/auth/",
#     client_id="fastapi",
#     client_secret="qNnqdLpdZgPvpxXmknz3D65r5tIx5S8k",
#     admin_client_secret="89Hz8ZQF3dh0diOGI7fnld9VXw18PNVo",
#     realm="fast",
#     callback_uri="http://localhost:8080/docs"
# )


# idp.add_swagger_config(app)

# @app.get("/login")
# def login_redirect():
#     return RedirectResponse(idp.login_uri)



# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl="http://0.0.0.0:8090/auth/realms/fast/protocol/openid-connect/auth",
#     tokenUrl="http://0.0.0.0:8090/auth/realms/fast/protocol/openid-connect/token", # https://sso.example.com/auth/realms/example-realm/protocol/openid-connect/token
# )

SECRET_KEY = "cacc7099dcedff3ac82b0f225533f81439871f5952f39f555f02fc45a2bfa12c"
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

def Authenticate(form_data: LoginUser,db:Session = Depends(get_db)):
    db_user = crud.get_userbyusername(db=db,username=form_data.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    
    hashed_password = hash_pass=hashlib.md5(form_data.password.encode('utf-8')).hexdigest()
    if not hashed_password == db_user.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return db_user
#https://codevoweb.com/restful-api-with-python-fastapi-access-and-refresh-tokens/
#for login lgoout



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



@app.post("/logout")
def logout(token: Annotated[str,Depends(oauth2_scheme)],db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
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
    # Revoke the token by adding it to the revoked_tokens table    
    revoke_token = revoke_token(is_expired=False,id=random.randint(10000,99999),token=token,user_id=random.randint(1,50),revoked_at=datetime.now)
    revoke_token_db=crud.create_revoke_token(db=db,token=revoke_token)
    return JSONResponse(content=revoke_token_db,status_code=status.HTTP_202_ACCEPTED)



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
             crud.update_advers(db=db,db_advers=advers1,updateadvers=advers_update)
             return status.HTTP_202_ACCEPTED
        else:
             raise credentials_exception
    except JWTError:
        raise credentials_exception

