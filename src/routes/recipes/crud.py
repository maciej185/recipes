"""CRUD operations for the recipes package."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.models import DB_Unit

from .models import UnitAdd


def add_measurment_unit(db: Session, unit_data: UnitAdd) -> DB_Unit:
    """Add a new measurment unit."""
    unit = DB_Unit(**unit_data.model_dump())
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


def delete_measurment_unit(db: Session, unit_id: int) -> bool:
    """Delete a measurment unit.

    Raises:
        HTTPException: Raises when a unit with the given ID
                was not found in the DB.

    Returns:
        Boolean information about whether or not the user was
        deleted.
    """
    unit = db.query(DB_Unit).filter(DB_Unit.unit_id == unit_id).first()
    if unit is None:
        raise HTTPException(
            status_code=404, detail="Unit with the given ID was nout found in the DB."
        )
    db.delete(unit)
    db.commit()
    return True
