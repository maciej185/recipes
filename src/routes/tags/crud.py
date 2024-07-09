"""CRUD operations for the tags package."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.models import DB_Tag, DB_User

from .models import TagAdd


def add_tag_to_db(db: Session, tag_data: TagAdd) -> DB_Tag:
    """Add a Tag to the DB with the given info."""
    db_tag = DB_Tag(**tag_data.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag_from_db(db: Session, tag_id: int) -> None:
    """Delete tag with the given ID from DB.

    Raises:
        HTTPException: Raises when a tag with the given ID
                was not found in the DB.
    """
    recipe = db.query(DB_Tag).filter(DB_Tag.tag_id == tag_id).first()
    if recipe is None:
        raise HTTPException(
            status_code=404, detail="Tag with the given ID was nout found in the DB."
        )
    return recipe


def list_tags_from_db(db: Session) -> list[DB_Tag]:
    """List all available tags in the DB."""
    return db.query(DB_Tag).all()


def add_tag_to_a_user(db: Session, tag_id: int, db_user: DB_User) -> DB_User:
    """Assign a  tag to a User and return the refreshed user object.

    Raises:
        HTTPException: Raised when a Tag with the given ID does not exist.
    """
    tag = db.query(DB_Tag).filter(DB_Tag.tag_id == tag_id).first()
    if tag is None:
        raise HTTPException(
            status_code=404, detail="Tag with the given ID was nout found in the DB."
        )
    db_user.tags.append(tag)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_tag_from_users_list(db: Session, tag_id: int, db_user: DB_User) -> DB_User:
    """Delete a tag from the user's list of subscribed tags and return the refreshed user object.

    Raises:
        HTTPException: Raised when
                        - a Tag with the given ID does not exist.
                        - a Tag with the given ID is not present on
                        the given User's list of subscribed tags.
    """
    tag = db.query(DB_Tag).filter(DB_Tag.tag_id == tag_id).first()
    if tag is None:
        raise HTTPException(
            status_code=404, detail="Tag with the given ID was nout found in the DB."
        )
    try:
        db_user.tags.remove(tag)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Tag with the given ID was nout found in the User's list of subscribed tags.",
        )
    db.commit()
    db.refresh(db_user)
    return db_user
