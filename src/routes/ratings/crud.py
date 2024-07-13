"""CRUD operations for the ratingd package."""

from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db.models import DB_Rating
from src.dependencies import get_db

from .models import RatingAdd


def create_rating_in_db(db: Session, rating_data: RatingAdd, author_id: int) -> DB_Rating:
    """Create a rating based on provided info."""
    db_rating = DB_Rating(**rating_data.model_dump(), author_id=author_id)
    db.add(db_rating)
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rating for the given recipe by the given user already exists.",
        )
    db.refresh(db_rating)
    return db_rating


def get_rating_from_db(
    rating_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]
) -> DB_Rating:
    """Get rating with the given ID.

    Used as a dependedncy in path operations.

    Raises:
        HTTPException: Raised when a rating with the given ID was not found in the DB.
    """
    db_rating = db.query(DB_Rating).filter(DB_Rating.rating_id == rating_id).first()
    if db_rating is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating with the given ID was not found in the DB.",
        )
    return db_rating


def delete_rating_from_db(db: Session, rating: DB_Rating) -> None:
    """Delete given rating from DB."""
    db.delete(rating)
    db.commit()


def list_ratings_from_db(db: Session) -> list[DB_Rating]:
    """List all avilable ratings from DB."""
    return db.query(DB_Rating).all()
