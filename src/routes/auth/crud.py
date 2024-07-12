"""CRUD operations for the auth package."""

from pathlib import Path
from typing import Optional

from fastapi import HTTPException, status
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


def get_all_users_from_db(db: Session) -> list[DB_User]:
    """List all users in the DB."""
    return db.query(DB_User).all()


def get_user_from_db(db: Session, user_id: int) -> DB_User:
    """Get a specific user from the DB."""
    user = db.query(DB_User).filter(DB_User.user_id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404, detail="User with the given ID does not exist in the DB."
        )
    return user


def follow_user_in_db(db: Session, follower_db_user: DB_User, followed_user_id: int) -> bool:
    """Follow user with the given ID.

    Args:
        follower_db_user: An instance of the DB_User model representing
                        the User that aims to follow another User.
        followed_user_id: ID of the User that will be followed by the previous User.

    Raises:
        HTTPException: Raised when
                        - the `follower_db_user` has the same ID
                          as `followed_user_id`
                        - a user with the given `followed_user_id`
                          was not found in the DB.
                        - the `follower_db_user` already follows the
                          user with the given `followed_user_id`


    Returns:
        Booelan information about whether or not the operation was successfull.
    """
    if follower_db_user.user_id == followed_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Users can't follow themselves."
        )
    db_followed_user = db.query(DB_User).filter(DB_User.user_id == followed_user_id).first()
    if db_followed_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with the given ID was not found in the DB.",
        )
    if db_followed_user in follower_db_user.followed_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The first user already follows the second one.",
        )
    follower_db_user.followed_users.append(db_followed_user)
    db.commit()
    db.refresh(follower_db_user)
    return True


def unfollow_user_in_db(db: Session, follower_db_user: DB_User, followed_user_id: int):
    """Unfollow a user with the given ID.

    Args:
        follower_db_user: An instance of the DB_User model representing
                        the User that aims to unfollow another User.
        followed_user_id: ID of the User that will be unfollowed by the previous User.

    Raises:
        HTTPException: Raised when
                        - the `follower_db_user` has the same ID
                          as `followed_user_id`
                        - a user with the given `followed_user_id`
                          was not found in the DB.
                        - the user with the given `followed_user_id`
                          was not followed by the `follower_db_user`
                          in the first place.
    Returns:
        Booelan information about whether or not the operation was successfull.
    """
    if follower_db_user.user_id == followed_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Users can't follow themselves."
        )
    db_followed_user = db.query(DB_User).filter(DB_User.user_id == followed_user_id).first()
    if db_followed_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with the given ID was not found in the DB.",
        )
    try:
        follower_db_user.followed_users.remove(db_followed_user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user was not followed."
        )
    db.commit()
    return True


def get_followers_from_db(db: Session, user_id: int) -> list[DB_User]:
    """Get all users following the user with the given ID.

    Raises:
        HTTPException: Raised when the user with the given ID
                        is not found in the DB.
    """
    db_user = db.query(DB_User).filter(DB_User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with the given ID was not found in the DB.",
        )
    return [user for user in db_user.followers]


def get_followed_users_from_db(db: Session, user_id: int) -> list[DB_User]:
    """Get all users that the user with the given ID follows.

    Raises:
        HTTPException: Raised when the user with the given ID
                        is not found in the DB.
    """
    db_user = db.query(DB_User).filter(DB_User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with the given ID was not found in the DB.",
        )
    return [user for user in db_user.followed_users]


def update_users_profile_pic_path(db: Session, user_id: int, profile_pic_path: Path) -> DB_User:
    """Update given user's profile pic path and return refreshed user object.

    Raises:
        HTTPException: Raised when the user with the given ID
                        is not found in the DB.
    """
    db_user = db.query(DB_User).filter(DB_User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with the given ID was not found in the DB.",
        )
    db_user.profile_pic_path = str(profile_pic_path)
    db.commit()
    db.refresh(db_user)
    return db_user
