"""CRUD operations for the tags package."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.models import DB_Tag

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
