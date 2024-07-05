"""Package with authentication-related endpoints."""

from .admin import admin_router
from .endpoints import router

__all__ = ["router" "admin_router"]
