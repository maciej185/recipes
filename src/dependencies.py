"""Dependencies for the app."""

from typing import Generator

from sqlalchemy.orm import Session

from src.db import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Get DB session and close it after the response was delivered."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
