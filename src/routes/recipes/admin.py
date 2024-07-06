"""Endpoints for the recipes package FOR ADMINS."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.orm import Session

from src.db.models import DB_Unit
from src.dependencies import get_db
from src.roles import Roles
from src.routes.auth.utils import RoleChecker
from src.tags import Tags

from .crud import add_measurment_unit, delete_measurment_unit, delete_recipe_from_db
from .models import Unit, UnitAdd

admin_router = APIRouter(
    prefix="/recipes",
    tags=[Tags.admin.value],
    dependencies=[Depends(RoleChecker([Roles.ADMIN.value]))],
)


@admin_router.post("/unit/add", response_model=Unit)
def add_unit(
    unit_data: Annotated[UnitAdd, Body()], db: Annotated[Session, Depends(get_db)]
) -> DB_Unit:
    """Add a measurment unit."""
    return add_measurment_unit(db=db, unit_data=unit_data)


@admin_router.delete("/unit/delete/{unit_id}", status_code=204)
def delete_unit(unit_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]) -> None:
    """Delete a measurment unit."""
    delete_measurment_unit(db=db, unit_id=unit_id)


@admin_router.delete("/recipe/delete/{recipe_id}", status_code=204)
def delete_recipe(
    recipe_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]
) -> None:
    """Delete a given recipe."""
    delete_recipe_from_db(db=db, recipe_id=recipe_id)
