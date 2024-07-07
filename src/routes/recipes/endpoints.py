"""Endpoints for the recipes package."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.orm import Session

from src.db.models import DB_Recipe, DB_Unit
from src.dependencies import get_db
from src.roles import Roles
from src.routes.auth.utils import RoleChecker
from src.tags import Tags

from .crud import add_recipe_to_db, get_recipe_from_db, list_measurment_units
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
    status_code=201,
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
