"""Endpoints for the auth package."""

from typing import Annotated, Literal

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db.models import DB_User
from src.dependencies import get_db
from src.roles import Roles
from src.tags import Tags

from .crud import (
    create_user,
    delete_user_from_db,
    follow_user_in_db,
    get_followed_users_from_db,
    get_followers_from_db,
    unfollow_user_in_db,
    update_user_in_db,
)
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


@router.get(
    "/me",
    response_model=UserInResponse,
    dependencies=[Depends(RoleChecker(allowed_roles=[Roles.USER.value]))],
)
async def read_users_me(
    current_user: Annotated[DB_User, Depends(get_current_user)],
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
    if updated_user is None:
        raise HTTPException(
            status_code=404, detail="User with the given ID does not exists in the database."
        )
    return updated_user


@router.post(
    "/follow/{followed_user_id}",
    dependencies=[Depends(RoleChecker([Roles.USER.value, Roles.ADMIN.value]))],
)
def follow_user(
    followed_user_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[DB_User, Depends(get_current_user)],
) -> dict[Literal["success"], bool]:
    """Endpoint for following other users."""
    return {
        "success": follow_user_in_db(
            db=db, follower_db_user=current_user, followed_user_id=followed_user_id
        )
    }


@router.post(
    "/unfollow/{followed_user_id}",
    dependencies=[Depends(RoleChecker([Roles.USER.value, Roles.ADMIN.value]))],
)
def unfollow_user(
    followed_user_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[DB_User, Depends(get_current_user)],
) -> dict[Literal["success"], bool]:
    """Endpoint for unfollowing other users."""
    return {
        "success": unfollow_user_in_db(
            db=db, follower_db_user=current_user, followed_user_id=followed_user_id
        )
    }


@router.get(
    "/followers/{user_id}",
    response_model=list[UserInResponse],
)
def get_followers(
    user_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]
) -> list[DB_User]:
    """Get all users following the user with the given ID."""
    return get_followers_from_db(db=db, user_id=user_id)


@router.get(
    "/followed/{user_id}",
    response_model=list[UserInResponse],
)
def get_followed_users(
    user_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]
) -> list[DB_User]:
    """Get all users that the user with the given ID follows."""
    return get_followed_users_from_db(db=db, user_id=user_id)
