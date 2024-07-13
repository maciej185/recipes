"""Pydantic models for the recipes package."""

from pydantic import BaseModel

from src.routes.ratings.models import Rating
from src.routes.tags.models import Tag


class InstructionBase(BaseModel):
    """Base for an instruction representation."""

    text: str
    order: int


class InstructionAdd(InstructionBase):
    """Model for adding a new instruction."""


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

    unit_id: int


class Ingredient(IngredientBase):
    """Model with all the ingredient information."""

    unit: Unit

    class Config:
        from_attributes = True


class NutritionInfoBase(BaseModel):
    """Base for a nutrition info representation."""

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

    nutritio_info_id: int
    calories: int = 0
    protein: int = 0
    carbohydrates: int = 0
    sugar: int = 0
    fiber: int = 0
    fat: int = 0


class NutritionInfoAdmin(NutritionInfoBase):
    """Model with all the nutrition info information for admins.

    The difference between this model and the one for standard
    users is that this contains the ID of the recipe and the ID
    of the DB_NutritionInfo object itself which might get useful
    when listing all the nutrition infos separately from the recipes.
    """

    recipe_id: int
    nutritio_info_id: int


class RecipeBase(BaseModel):
    """Base for a recipe representation."""

    # name: str
    servings: int
    prep_time: int
    description: str


class RecipeAdd(RecipeBase):
    """Model for adding a new recipe."""

    author_id: int
    ingredients: list[IngredientAdd]
    instructions: list[InstructionAdd]
    nutrition_info: NutritionInfoAdd
    tags: list[int] | None = None


class Recipe(RecipeBase):
    """Model with all the recipe information."""

    recipe_id: int
    author_id: int
    ingredientes: list[Ingredient] = []
    instructions: list[Instruction] = []
    nutrition_info: list[NutritionInfo]
    tags: list[Tag]
    ratings: list[Rating]

    class Config:
        from_attributes = True
