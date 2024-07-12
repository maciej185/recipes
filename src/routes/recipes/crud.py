"""CRUD operations for the recipes package."""

from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.db.models import (
    DB_Ingredient,
    DB_Instruction,
    DB_NutritionInfo,
    DB_Recipe,
    DB_RecipeImage,
    DB_Tag,
    DB_Unit,
    DB_User,
)

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
    tags = recipe_dict.pop("tags")
    db_recipe = DB_Recipe(**recipe_dict)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    add_instructions_to_db(db=db, instructions_data=instructions, recipe_id=db_recipe.recipe_id)
    add_ingredients_to_db(db=db, ingredients_data=ingredients, recipe_id=db_recipe.recipe_id)
    add_nutrition_info_to_db(
        db=db, nutrition_info_data=nutrition_info, recipe_id=db_recipe.recipe_id
    )
    db_recipe = (
        add_tags_to_a_recipe(db=db, tag_ids=tags, db_recipe=db_recipe) if tags else db_recipe
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


def add_tags_to_a_recipe(db: Session, tag_ids: list[int], db_recipe: DB_Recipe) -> DB_Recipe:
    """Add tags to a given recipe and return the refreshed recipe object with tags included."""
    tags = [db.query(DB_Tag).filter(DB_Tag.tag_id == tag_id).first() for tag_id in tag_ids]
    for tag in tags:
        if tag:
            db_recipe.tags.append(tag)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


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


def add_recipe_to_saved_list(db: Session, recipe_id: int, db_user: DB_User) -> DB_User:
    """Add recipe to user's saved recipe list and return a refreshed user object.

    Raises:
        HTTPException: Raised when
                    - a Recipe with the given ID was not found in the DB.
                    - a Recipve with the given ID was already saved by the User.
    """
    recipe = db.query(DB_Recipe).filter(DB_Recipe.recipe_id == recipe_id).first()
    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe with the given ID does not exist in the DB.",
        )
    if recipe in db_user.saved_recipes:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Recipe already saved.")
    db_user.saved_recipes.append(recipe)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_recipe_from_users_saved_list(db: Session, recipe_id: int, db_user: DB_User) -> DB_User:
    """Delete a recipe from the user's list of saved recipes and return the refreshed user object.

    Raises:
        HTTPException: Raised when
                        - a Recipe with the given ID does not exist.
                        - a Recipe with the given ID is not present on
                        the given User's list of subscribed tags.
    """
    recipe = db.query(DB_Recipe).filter(DB_Recipe.recipe_id == recipe_id).first()
    if recipe is None:
        raise HTTPException(
            status_code=404, detail="Recipe with the given ID was nout found in the DB."
        )
    try:
        db_user.saved_recipes.remove(recipe)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Recipe with the given ID was nout found in the User's list of saved recipes.",
        )
    db.commit()
    db.refresh(db_user)
    return db_user


def save_recipe_images_in_db(
    db: Session, recipe_id: int, recipe_images_paths: list[Path]
) -> list[DB_RecipeImage]:
    """Save info about images for a given recipe in the DB."""
    db_recipe_images = []
    for recipe_images_path in recipe_images_paths:
        db_recipe_image = DB_RecipeImage(recipe_id=recipe_id, image_path=recipe_images_path)
        db.add(db_recipe_image)
        db.commit()
        db.refresh(db_recipe_image)
        db_recipe_images.append(db_recipe_image)
    return db_recipe_images


def get_recipe_image_from_db(db: Session, recipe_image_id: int) -> DB_RecipeImage:
    """Get recipe image with the given ID.

    Raises:
        HTTPException: Raised when a recipe image with the given ID was not found in the DB.
    """
    db_recipe_image = (
        db.query(DB_RecipeImage).filter(DB_RecipeImage.recipe_image_id == recipe_image_id).first()
    )
    if db_recipe_image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image with the given ID was not found in the DB.",
        )
    return db_recipe_image
