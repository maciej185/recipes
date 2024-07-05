"""Endpoints for the auth package FOR ADMINS."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from src.db.models import DB_User
from src.dependencies import get_db
from src.roles import Roles
from src.tags import Tags

from .crud import delete_user_from_db, get_all_users_from_db, get_user_from_db
from .models import UserInResponseAdmin
from .utils import RoleChecker

admin_router = APIRouter(prefix="/auth", tags=[Tags.admin.value])


@admin_router.delete("/delete/{user_id}")
def delete_user(
    user_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Roles.ADMIN.value]))],
) -> dict[str, bool]:
    """Delete user with the given ID."""
    return {"success": delete_user_from_db(db=db, user_id=user_id)}


@admin_router.get("/get/user/{user_id}", response_model=UserInResponseAdmin)
def get_user(
    user_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Roles.ADMIN.value]))],
) -> DB_User:
    """Get user with the given ID."""
    return get_user_from_db(db=db, user_id=user_id)


@admin_router.get("/get/users", response_model=list[UserInResponseAdmin])
def get_users(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Roles.ADMIN.value]))],
) -> list[DB_User]:
    """Get a list of all users from the DB."""
    return get_all_users_from_db(db=db)
