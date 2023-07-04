from fastapi import FastAPI
app = FastAPI()
from routes.user import router
app = FastAPI()
app.include_router(router)
