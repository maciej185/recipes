"""Endpoints for the recipes package FOR ADMINS."""

from fastapi import APIRouter, Depends

from src.roles import Roles
from src.routes.auth.utils import RoleChecker
from src.tags import Tags

admin_router = APIRouter(
    prefix="/tags",
    tags=[Tags.admin.value],
    dependencies=[Depends(RoleChecker([Roles.ADMIN.value]))],
)
