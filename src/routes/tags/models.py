"""Pydantic models for the recipes package."""

from pydantic import BaseModel


class TagBase(BaseModel):
    """Base model for Tags."""

    name: str


class TagAdd(TagBase):
    """Model for adding new Tags."""


class Tag(TagBase):
    """Model with all the Tag info."""

    tag_id: int
