from fastapi import FastAPI
app = FastAPI()
from routes.user import user
app = FastAPI()
app.include_router(user)
