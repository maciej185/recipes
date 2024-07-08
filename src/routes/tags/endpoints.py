"""Endpoints for the recipes package."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.models import DB_Tag
from src.dependencies import get_db
from src.tags import Tags

from .crud import list_tags_from_db
from .models import Tag

router = APIRouter(prefix="/tags", tags=[Tags.tags])


@router.get("/list", response_model=list[Tag])
def tag_list(db: Annotated[Session, Depends(get_db)]) -> list[DB_Tag]:
    """List all available tags"""
    return list_tags_from_db(db=db)
