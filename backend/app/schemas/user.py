from datetime import datetime

from pydantic import BaseModel, EmailStr, constr


class User(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
        from_attributes = True
