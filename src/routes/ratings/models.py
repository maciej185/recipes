"""Pydantic models for the ratings package."""

from pydantic import BaseModel


class RatingBase(BaseModel):
    """Base for a recipe representation."""

    rating: float
    recipe_id: int


class RatingAdd(RatingBase):
    """Model for adding a new rating."""


class Rating(RatingBase):
    """Model with all the rating information."""

    rating_id: int
    author_id: int
