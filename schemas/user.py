from pydantic import BaseModel
from typing import Optional
class User(BaseModel):
    id: Optional[int]
    username: str
    password: str
    phone: int
    isactivate: bool = True
    class Config:
        orm_mode = True

