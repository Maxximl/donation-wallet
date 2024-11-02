from enum import Enum
import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship

from .base import BaseTable


class Account(BaseTable):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    balance = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
