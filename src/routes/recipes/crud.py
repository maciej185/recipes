"""CRUD operations for the recipes package."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.models import DB_Recipe, DB_Unit

from .models import UnitAdd


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
