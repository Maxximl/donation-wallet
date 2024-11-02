from pydantic import BaseModel


class Account(BaseModel):
    id: int
    balance: float
    owner_id: int

    class Config:
        orm_mode = True
        from_attributes = True
