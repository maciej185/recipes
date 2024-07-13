"""CRUD operations for the ratingd package."""

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db.models import DB_Rating

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
