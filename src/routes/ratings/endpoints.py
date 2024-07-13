"""Endpoints for the ratings package."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from src.db.models import DB_Rating, DB_User
from src.dependencies import get_db
from src.roles import Roles
from src.routes.auth.utils import RoleChecker, get_current_user
from src.tags import Tags

from .crud import create_rating_in_db, delete_rating_from_db, get_rating_from_db
from .models import Rating, RatingAdd

router = APIRouter(prefix="/ratings", tags=[Tags.ratings.value])


@router.post(
    "/add",
    response_model=Rating,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleChecker(allowed_roles=[Roles.ADMIN.value, Roles.USER.value]))],
)
def add_rating(
    rating_data: Annotated[RatingAdd, Body()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[DB_User, Depends(get_current_user)],
) -> DB_Rating:
    """Add a new rating for a recipe.

    Raises:
        HTTPException: Raised when the user attempting to rate the recipe is the
                        recipe's author.
    """
    from src.routes.recipes.crud import (
        get_recipe_from_db,
    )  # imported in the function's body to avoid circular imports

    db_recipe = get_recipe_from_db(db=db, recipe_id=rating_data.recipe_id)
    if db_recipe.author_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authenticated user is the author of the recipe which prohibits them from ratings.",
        )
    return create_rating_in_db(db=db, rating_data=rating_data, author_id=current_user.user_id)


@router.delete(
    "/delete/{rating_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RoleChecker(allowed_roles=[Roles.ADMIN.value, Roles.USER.value]))],
)
def rating_delete(
    rating: Annotated[DB_Rating, Depends(get_rating_from_db)],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[DB_User, Depends(get_current_user)],
) -> None:
    """Delete rating with the given ID.

    Raises:
        HTTPException: Raised when the authenticated user is not the the author of the
                        rating.
    """
    if current_user.user_id != rating.author_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The authenticated user is not the author of the rating.",
        )
    delete_rating_from_db(db=db, rating=rating)
