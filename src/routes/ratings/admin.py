"""Endpoints for the auth package FOR ADMINS."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.models import DB_Rating
from src.dependencies import get_db
from src.roles import Roles
from src.routes.auth.utils import RoleChecker
from src.tags import Tags

from .crud import delete_rating_from_db, get_rating_from_db, list_ratings_from_db
from .models import Rating

admin_router = APIRouter(
    prefix="/ratings",
    tags=[Tags.admin.value],
    dependencies=[Depends(RoleChecker(allowed_roles=[Roles.ADMIN.value]))],
)


@admin_router.get("/list", response_model=list[Rating])
def list_ratings(db: Annotated[Session, Depends(get_db)]) -> list[DB_Rating]:
    """List all available ratings."""
    return list_ratings_from_db(db=db)


@admin_router.delete("/delete_admin/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(
    rating: Annotated[DB_Rating, Depends(get_rating_from_db)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    """Delete rating with the given ID."""
    delete_rating_from_db(db=db, rating=rating)
