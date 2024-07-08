"""Endpoints for the recipes package."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from src.db.models import DB_Tag, DB_User
from src.dependencies import get_db
from src.roles import Roles
from src.routes.auth.utils import RoleChecker, get_current_user
from src.tags import Tags

from .crud import add_tag_to_a_user, list_tags_from_db
from .models import Tag

router = APIRouter(prefix="/tags", tags=[Tags.tags])


@router.get(
    "/list",
    response_model=list[Tag],
    dependencies=[Depends(RoleChecker([Roles.USER.value, Roles.ADMIN.value]))],
)
def tag_list(db: Annotated[Session, Depends(get_db)]) -> list[DB_Tag]:
    """List all available tags"""
    return list_tags_from_db(db=db)


@router.post("/subscribe/{tag_id}", status_code=201)
def subscribe_to_tag(
    tag_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[DB_User, Depends(get_current_user)],
) -> None:
    """Let the current user subscribe to a given Tag."""
    add_tag_to_a_user(db=db, tag_id=tag_id, db_user=current_user)
