from fastapi import FastAPI
app = FastAPI(root_path="/main")
from routes.user import router
app.include_router(router)
