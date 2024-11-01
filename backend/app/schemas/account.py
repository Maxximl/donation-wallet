from pydantic import BaseModel


class Account(BaseModel):
    id: int
    balance: float
