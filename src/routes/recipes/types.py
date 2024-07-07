"""Types for the recipes package."""

from typing import TypedDict


class IngredientAddDict(TypedDict):
    """Dictionary with the same info as the IngredientAdd model."""

    ingredient: str
    amount: float
    unit_id: int


class InstructionAddDict(TypedDict):
    """Dictionary with the same info as the InstructionAdd model."""

    text: str
    order: int


class NutritionInfoAddDict(TypedDict):
    """Dictionary with the same info as the NutritionInfoAdd model."""

    calories: int
    protein: int
    carbohydrates: int
    sugar: int
    fiber: int
    fat: int
