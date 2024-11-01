from enum import Enum
import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship

from .base import BaseTable


class CharityOrganization(BaseTable):
    __tablename__ = 'charity_organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    website = Column(String)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String)
    address = Column(String)

    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    account = relationship("Account")
