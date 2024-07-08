"""Package with tag-related endpoints."""

from .admin import admin_router
from .endpoints import router

__all__ = ["admin_router", "router"]
