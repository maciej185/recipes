"""Pydantic models for the auth package."""

from datetime import date

from pydantic import BaseModel

from src.roles import Roles


class UserBase(BaseModel):
    """Base for User models."""

    username: str
    email: str
    first_name: str
    last_name: str
    date_of_birth: date
    description: str | None

    class Config:
        from_attributes = True


class UserAdd(UserBase):
    """Model for adding users."""

    plain_text_password: str


class UserInResponse(UserBase):
    """Model for returning User information."""

    user_id: int
    role: Roles


class UserUpdate(UserBase):
    """Model for updating the User info."""

    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: str | date = None
    description: str | None = None


class Token(BaseModel):
    """Model with token information."""

    access_token: str
    token_type: str
