"""Endpoints for the recipes package."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, UploadFile, status
from sqlalchemy.orm import Session

from src.db.models import DB_Recipe, DB_Unit, DB_User
from src.dependencies import get_db
from src.roles import Roles
from src.routes.auth.utils import RoleChecker, get_current_user
from src.tags import Tags
from src.utils import FileStorageManager

from .crud import (
    add_recipe_to_db,
    add_recipe_to_saved_list,
    delete_recipe_from_db,
    delete_recipe_from_users_saved_list,
    get_recipe_from_db,
    list_measurment_units,
    save_recipe_images_in_db,
)
from .models import Recipe, RecipeAdd, Unit

router = APIRouter(
    prefix="/recipes",
    tags=[Tags.recipes],
)


@router.post(
    "/units/list",
    response_model=list[Unit],
    dependencies=[Depends(RoleChecker([Roles.USER.value, Roles.ADMIN.value]))],
)
def list_units(db: Annotated[Session, Depends(get_db)]) -> list[DB_Unit]:
    """List all available units."""
    return list_measurment_units(db=db)


@router.post(
    "/recipe/add",
    response_model=Recipe,
    dependencies=[Depends(RoleChecker([Roles.USER.value, Roles.ADMIN.value]))],
    status_code=status.HTTP_201_CREATED,
)
def add_recipe(
    recipe_data: Annotated[RecipeAdd, Body()], db: Annotated[Session, Depends(get_db)]
) -> DB_Recipe:
    """Add a new recipe."""
    return add_recipe_to_db(db=db, recipe_data=recipe_data)


@router.get("/recipe/{recipe_id}", response_model=Recipe)
def get_recipe(
    recipe_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]
) -> DB_Recipe:
    """Return a recipe with the given ID."""
    return get_recipe_from_db(db=db, recipe_id=recipe_id)


@router.delete(
    "/recipe/delete/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RoleChecker([Roles.USER.value, Roles.ADMIN.value]))],
)
def delete_recipe(
    recipe_id: Annotated[int, Path],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[DB_User, Depends(get_current_user)],
) -> None:
    """Delete recipe with the given ID.

    Raises:
        HTTPException: Raised when the currently logged in user is not the owner
        of the recipe with the given ID.
    """
    recipe = get_recipe_from_db(db=db, recipe_id=recipe_id)
    if current_user.user_id != recipe.author_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Current user it not the owner of the Recipe.",
        )
    delete_recipe_from_db(db=db, recipe_id=recipe_id)


@router.post(
    "/saved/save/{recipe_id}",
    dependencies=[Depends(RoleChecker([Roles.USER.value, Roles.ADMIN.value]))],
    status_code=201,
)
def save_recipe(
    recipe_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[DB_User, Depends(get_current_user)],
) -> None:
    """Allow users to save recipes for later."""
    add_recipe_to_saved_list(db=db, recipe_id=recipe_id, db_user=current_user)


@router.delete(
    "/saved/delete/{recipe_id}",
    dependencies=[Depends(RoleChecker([Roles.USER.value, Roles.ADMIN.value]))],
    status_code=204,
)
def delete_recipe_from_saved(
    recipe_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[DB_User, Depends(get_current_user)],
) -> None:
    """Delete a recipe from the user's saved recipe list."""
    delete_recipe_from_users_saved_list(db=db, recipe_id=recipe_id, db_user=current_user)


@router.post(
    "/recipe/pictures/upload/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RoleChecker(allowed_roles=[Roles.USER.value, Roles.ADMIN.value]))],
)
def upload_recipe_images(
    recipe_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    recipe_images_files: Annotated[list[UploadFile], File()],
    current_user: Annotated[DB_User, Depends(get_current_user)],
) -> None:
    """Upload images for a given recipe

    Raises:
        HTTPException: Raised when the currently logged in user is not the author
                        of the recipe.
    """
    db_recipe = get_recipe_from_db(db=db, recipe_id=recipe_id)
    if current_user.user_id != db_recipe.author.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Currently authenticated user is not the author of the recipe.",
        )
    recipe_images_paths = FileStorageManager.save_recipe_images(
        recipe_id=recipe_id, uploaded_files=recipe_images_files
    )
    save_recipe_images_in_db(db=db, recipe_id=recipe_id, recipe_images_paths=recipe_images_paths)
