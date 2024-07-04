"""Utils for the auth package."""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.db.models import DB_User
from src.dependencies import get_db
from src.utils import ConfigManager

config = ConfigManager.get_config()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password, hashed_password) -> bool:
    """Verify if the provided password matches the hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    """Generate a hash for the given password."""
    return pwd_context.hash(password)


def get_user(db: Session, username: str) -> Optional[DB_User]:
    """Get user from the DB."""
    return db.query(DB_User).filter(DB_User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> Union[bool, DB_User]:
    """Authenticate the user based on the given username and password."""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict) -> str:
    """Create JWT based on the provided JSON"""
    to_encode = data.copy()
    encoded_jwt = jwt.encode(
        to_encode, config.token_signing_key, algorithm=config.token_signing_algorithm
    )
    return encoded_jwt


def get_current_user(
    db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]
) -> DB_User:
    """Authenticate the user and return the object representing them based on the token provided in the header."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.token_signing_key, algorithms=[config.token_signing_algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user


class RoleChecker:
    """DEpendency for checking the permissions of the currently logged in user."""

    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[DB_User, Depends(get_current_user)]):
        if user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't have enough permissions"
        )
