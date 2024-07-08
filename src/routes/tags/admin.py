"""Endpoints for the recipes package FOR ADMINS."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from src.db.models import DB_Tag
from src.dependencies import get_db
from src.roles import Roles
from src.routes.auth.utils import RoleChecker
from src.tags import Tags

from .crud import add_tag_to_db, delete_tag_from_db
from .models import Tag, TagAdd

admin_router = APIRouter(
    prefix="/tags",
    tags=[Tags.admin],
    dependencies=[Depends(RoleChecker([Roles.ADMIN.value]))],
)


@admin_router.post("/add", response_model=Tag, status_code=status.HTTP_201_CREATED)
def tag_add(tag_data: Annotated[TagAdd, Body()], db: Annotated[Session, Depends(get_db)]) -> DB_Tag:
    """Add tag based on the provided info."""
    return add_tag_to_db(db=db, tag_data=tag_data)


@admin_router.delete("/delete/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def tag_delete(tag_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]) -> None:
    """Delete tag with the given ID."""
    delete_tag_from_db(db=db, tag_id=tag_id)
