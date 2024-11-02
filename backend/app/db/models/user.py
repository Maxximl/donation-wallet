from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT

from .base import BaseTable


class User(BaseTable):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(
        "username",
        TEXT,
        nullable=False,
        unique=True,
        index=True,
        doc="Username for authentication.",
    )
    password = Column(
        "password",
        TEXT,
        nullable=False,
        index=True,
        doc="Hashed password.",
    )
    email = Column(
        "email",
        TEXT,
        nullable=True,
        doc="Email for notifications.",
        unique=True,
    )
