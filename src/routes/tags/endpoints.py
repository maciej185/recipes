"""Endpoints for the recipes package."""

from fastapi import APIRouter

from src.tags import Tags

router = APIRouter(prefix="/tags", tags=Tags.tags.value)
