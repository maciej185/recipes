"""CRUD operations for the recipes package."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.models import DB_Ingredient, DB_Instruction, DB_NutritionInfo, DB_Recipe, DB_Unit

from .models import RecipeAdd, UnitAdd
from .types import IngredientAddDict, InstructionAddDict, NutritionInfoAddDict


def add_measurment_unit(db: Session, unit_data: UnitAdd) -> DB_Unit:
    """Add a new measurment unit."""
    unit = DB_Unit(**unit_data.model_dump())
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


def delete_measurment_unit(db: Session, unit_id: int) -> None:
    """Delete a measurment unit.

    Raises:
        HTTPException: Raises when a unit with the given ID
                was not found in the DB.
    """
    unit = db.query(DB_Unit).filter(DB_Unit.unit_id == unit_id).first()
    if unit is None:
        raise HTTPException(
            status_code=404, detail="Unit with the given ID was nout found in the DB."
        )
    db.delete(unit)
    db.commit()


def list_measurment_units(db: Session) -> list[DB_Unit]:
    """List all measurments unit available in the DB."""
    return db.query(DB_Unit).all()


def delete_recipe_from_db(db: Session, recipe_id: int) -> None:
    """Delete recipe from DB.

    Raises:
        HTTPException: Raises when a recipe with the given ID
                was not found in the DB.
    """
    recipe = db.query(DB_Recipe).filter(DB_Recipe.recipe_id == recipe_id).first()
    if recipe is None:
        raise HTTPException(
            status_code=404, detail="Recipe with the given ID was nout found in the DB."
        )
    db.delete(recipe)
    db.commit()


def get_recipe_from_db(db: Session, recipe_id: int) -> DB_Recipe:
    """Get recipe with the given ID from the DB.

    Raises:
        HTTPException: Raises when a recipe with the given ID
                was not found in the DB.
    """
    recipe = db.query(DB_Recipe).filter(DB_Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=404, detail="Recipe with the given ID was nout found in the DB."
        )
    return recipe


def add_recipe_to_db(db: Session, recipe_data: RecipeAdd) -> DB_Recipe:
    """Add recipe to the database."""
    recipe_dict = recipe_data.model_dump()
    instructions = recipe_dict.pop("instructions")
    ingredients = recipe_dict.pop("ingredients")
    nutrition_info = recipe_dict.pop("nutrition_info")
    db_recipe = DB_Recipe(**recipe_dict)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    add_instructions_to_db(db=db, instructions_data=instructions, recipe_id=db_recipe.recipe_id)
    add_ingredients_to_db(db=db, ingredients_data=ingredients, recipe_id=db_recipe.recipe_id)
    add_nutrition_info_to_db(
        db=db, nutrition_info_data=nutrition_info, recipe_id=db_recipe.recipe_id
    )

    return db_recipe


def add_instructions_to_db(
    db: Session, instructions_data: list[InstructionAddDict], recipe_id: int
) -> None:
    """Save instructions for the given recipe in the DB."""
    for instruction in instructions_data:
        db_instruction = DB_Instruction(**instruction, recipe_id=recipe_id)
        db.add(db_instruction)
        db.commit()
        db.refresh(db_instruction)


def add_ingredients_to_db(
    db: Session, ingredients_data: list[IngredientAddDict], recipe_id: int
) -> None:
    """Save ingredients for the given recipe in the DB."""
    for ingredient in ingredients_data:
        db_ingredient = DB_Ingredient(**ingredient, recipe_id=recipe_id)
        db.add(db_ingredient)
        db.commit()
        db.refresh(db_ingredient)


def add_nutrition_info_to_db(
    db: Session, nutrition_info_data: NutritionInfoAddDict, recipe_id: int
) -> None:
    """Save nutrition info for the given recipe in the DB."""
    db_nutrition_info = DB_NutritionInfo(**nutrition_info_data, recipe_id=recipe_id)
    db.add(db_nutrition_info)
    db.commit()
    db.refresh(db_nutrition_info)


def get_nutrition_info_from_db(db: Session, nutrition_info_id: int) -> DB_NutritionInfo:
    """Get a given nutrition info from the DB.

    Raises:
        HTTPException: Raised when a recipe with the given nutrition info
                was not found in the DB.
    """
    nutrition_info = (
        db.query(DB_NutritionInfo)
        .filter(DB_NutritionInfo.nutritio_info_id == nutrition_info_id)
        .first()
    )
    if nutrition_info is None:
        raise HTTPException(
            status_code=404, detail="Nutrition info with the given ID was nout found in the DB."
        )
    return nutrition_info


def list_nutrition_infos_from_db(db: Session) -> list[DB_NutritionInfo]:
    """List all available nutrition infos from the DB."""
    return db.query(DB_NutritionInfo).all()


def list_instructions_from_db(db: Session) -> list[DB_Instruction]:
    """List all available instructions from teh DB."""
    return db.query(DB_Instruction).all()


def list_ingredients_from_db(db: Session) -> list[DB_Ingredient]:
    """List all available ingredients from the DB."""
    return db.query(DB_Ingredient).all()
