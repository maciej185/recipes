"""ORM models for the app."""

from datetime import datetime

from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from src.roles import Roles

Base = declarative_base()


class DB_User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100))
    hashed_password = Column(String(150))
    first_name = Column(String(100))
    last_name = Column(String(100))
    description = Column(Text)
    create_date = Column(Date, default=datetime.now())
    date_of_birth = Column(Date)
    role = Column(Integer, default=Roles.USER.value)
