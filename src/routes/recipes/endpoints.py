"""Endpoints for the recipes package."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.models import DB_Unit
from src.dependencies import get_db
from src.roles import Roles
from src.routes.auth.utils import RoleChecker
from src.tags import Tags

from .crud import list_measurment_units
from .models import Unit

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
