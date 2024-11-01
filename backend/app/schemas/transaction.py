from pydantic import BaseModel, Field

from datetime import datetime

from enum import Enum


# class TransactionType(str, Enum):
#     donation = "donation"
#     deposit = "deposit"


class Transaction(BaseModel):
    id: int
    sender_account_id: int
    receiver_account_id: int
    amount: float
    description: str
    timestamp: datetime
    transaction_type: str