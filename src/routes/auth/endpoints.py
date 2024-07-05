"""Endpoints for the auth package."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db.models import DB_User
from src.dependencies import get_db
from src.roles import Roles
from src.tags import Tags

from .crud import create_user, delete_user_from_db, update_user_in_db
from .models import Token, UserAdd, UserInResponse, UserUpdate
from .utils import RoleChecker, authenticate_user, create_access_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=[Tags.auth],
)


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, str]:
    """Return access token if the user is authenticated."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserInResponse)
async def read_users_me(
    current_user: Annotated[DB_User, Depends(get_current_user)],
    _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Roles.USER.value]))],
) -> DB_User:
    """Return an object representing the currently logged in User."""
    return current_user


@router.post("/register", response_model=UserInResponse, status_code=201)
def register(
    user_data: Annotated[UserAdd, Body()], db: Annotated[Session, Depends(get_db)]
) -> DB_User:
    """Register the given User."""
    return create_user(db, user_data)


@router.put("/update", response_model=UserInResponse)
def update_user(
    user_data: Annotated[UserUpdate, Body()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[DB_User, Depends(get_current_user)],
) -> DB_User:
    """Update given User with the provided information"""
    updated_user = update_user_in_db(db, current_user.user_id, user_data)
    if update_user is None:
        raise HTTPException(
            status_code=404, detail="User with the given ID does not exists in the database."
        )
    return updated_user
