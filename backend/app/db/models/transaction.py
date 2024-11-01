from enum import Enum
import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship

from .base import BaseTable


class TransactionType(Enum):
    donation = "donation"
    deposit = "deposit"


class Transaction(BaseTable):
    __tablename__ = 'transactions'

    sender_account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    receiver_account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    transaction_type = Column(String, nullable=False)

    sender_account = relationship("Account", foreign_keys=[sender_account_id])
    receiver_account = relationship("Account", foreign_keys=[receiver_account_id])

    # sender_account = relationship("Account", foreign_keys=[sender_account_id], back_populates="sent_transactions")
    # receiver_account = relationship("Account", foreign_keys=[receiver_account_id], back_populates="received_transactions")
