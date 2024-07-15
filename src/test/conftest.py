"""General fixtures for the test suite."""

from datetime import datetime
from typing import Any, Generator

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db.models import DB_User
from src.dependencies import get_db
from src.main import app
from src.roles import Roles
from src.routes.auth.utils import get_password_hash

from .db import TestingSessionLocal, override_get_db


@pytest.fixture(autouse=True)
def override_get_db_for_each_test():
    """Override the 'get_db' dependency and return to original dependency after each test."""
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides = {}


@pytest.fixture()
def overriden_db() -> Generator[Session, Any, Any]:
    """Get overriden DB."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def register_user(overriden_db: Session):
    """Register a sample user in the DB."""
    hashed_password = get_password_hash("password")
    db_user = DB_User(
        username="username",
        first_name="first_name",
        last_name="last_name",
        hashed_password=hashed_password,
        email="email@email.com",
        date_of_birth=datetime.now().date(),
        description="Descritpion",
        role=Roles.USER.value,
    )
    overriden_db.add(db_user)
    try:
        overriden_db.commit()
    except IntegrityError:
        overriden_db.rollback()
        return overriden_db.query(DB_User).filter(DB_User.username == "username").first()
    overriden_db.refresh(db_user)
    return db_user
