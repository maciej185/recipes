"""CRUD operations for the auth package."""

from typing import Optional

from sqlalchemy.orm import Session

from src.db.models import DB_User
from src.roles import Roles

from .models import UserAdd, UserUpdate
from .utils import get_password_hash


def create_user(db: Session, user_data: UserAdd, role: int = Roles.USER.value) -> DB_User:
    """Save User and return it's DB representation."""
    hashed_password = get_password_hash(user_data.plain_text_password)
    db_user = DB_User(
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=hashed_password,
        email=user_data.email,
        date_of_birth=user_data.date_of_birth,
        description=user_data.description,
        role=role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_in_db(db: Session, user_id: int, user_data: UserUpdate) -> Optional[DB_User]:
    """Update the given User with the provided information."""
    db_user_query = db.query(DB_User).filter(DB_User.user_id == user_id)
    if db_user_query:
        user_dict = {k: v for k, v in user_data.model_dump().items() if not v is None}
        db_user_query.update(user_dict, synchronize_session=False)
        db.commit()
        db_user = db_user_query.first()
        db.refresh(db_user)
        return db_user


def delete_user_from_db(db: Session, user_id: int) -> bool:
    """Delete user with the given ID from DB.

    Returns:
        Boolean information about whether or not the user was deleted. The
        only situtation when it might not have been deleted is when it
        didn't exist in the first place.
    """
    user = db.query(DB_User).filter(DB_User.user_id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
