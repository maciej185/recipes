"""Pydantic models for the recipes package."""

from pydantic import BaseModel

from src.routes.auth.models import UserInResponse


class InstructionBase(BaseModel):
    """Base for an instruction representation."""

    text: str
    order: int


class InstructionAdd(InstructionBase):
    """Model for adding a new instruction."""

    recipe_id: int


class Instruction(InstructionBase):
    """Model with all instruction information."""

    instruction_id: int


class UnitBase(BaseModel):
    """Base for a measurment unit representation."""

    unit: str
    liquid: bool


class UnitAdd(UnitBase):
    """Model for adding a new measurment unit."""


class Unit(UnitBase):
    """Model with all measurment unit information."""

    unit_id: int


class IngredientBase(BaseModel):
    """Base for an ingredient representation."""

    ingredient: str
    amount: float


class IngredientAdd(IngredientBase):
    """Model for adding a new ingredient."""

    recipe_id: int
    unit_id: int


class Ingredient(IngredientBase):
    """Model with all the ingredient information."""

    unit: Unit

    class Config:
        from_attributes = True


class NutritionInfoBase(BaseModel):
    """Base for a nutrition info representation."""

    recipe_id: int
    calories: int
    protein: int
    carbohydrates: int
    sugar: int
    fiber: int
    fat: int


class NutritionInfoAdd(NutritionInfoBase):
    """Model for adding a new nutrition info object."""


class NutritionInfo(NutritionInfoBase):
    """Model with all the nutrition info information."""


class RecipeBase(BaseModel):
    """Base for a recipe representation."""

    name: str
    create_date: str
    servings: int
    prep_time: int
    description: str


class RecipeAdd(RecipeBase):
    """Model for adding a new recipe."""

    author_id: int
    ingredients: list[IngredientAdd]
    instructions: list[InstructionAdd]


class Recipe(RecipeBase):
    """Model with all the recipe information."""

    author: UserInResponse
    ingredientes: list[Ingredient]
    instructions: list[Instruction]
    nutrition_info: NutritionInfo

    class Config:
        from_attributes = True
