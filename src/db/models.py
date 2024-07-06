"""ORM models for the app."""

from datetime import datetime

from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.roles import Roles

Base = declarative_base()


class DB_User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100))
    hashed_password = Column(String(150))
    first_name = Column(String(100))
    last_name = Column(String(100))
    description = Column(Text)
    create_date = Column(Date, default=datetime.now())
    date_of_birth = Column(Date)
    role = Column(Integer, default=Roles.USER.value)

    recipes = relationship("DB_Recipe", back_populates="author")


class DB_Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    create_date = Column(Date, default=datetime.now(), nullable=False)
    servings = Column(Integer, nullable=False)
    prep_time = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    author = relationship("DB_User", back_populates="recipes")
    nutrition_info = relationship("DB_NutritionInfo", back_populates="recipe")
    instructions = relationship("DB_Instruction", back_populates="recipe")
    ingredientes = relationship("DB_Ingredient", back_populates="recipe")


class DB_NutritionInfo(Base):
    __tablename__ = "nutrition_infos"

    nutritio_info_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), nullable=False)
    calories = Column(Integer, nullable=False)
    protein = Column(Integer, nullable=False)
    carbohydrates = Column(Integer, nullable=False)
    sugar = Column(Integer, nullable=False)
    fiber = Column(Integer, nullable=False)
    fat = Column(Integer, nullable=False)

    recipe = relationship("DB_Recipe", back_populates="nutrition_info")


class DB_Instruction(Base):
    __tablename__ = "instructions"

    instruction_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), nullable=False)
    text = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)

    recipe = relationship("DB_Recipe", back_populates="instructions")


class DB_Unit(Base):
    __tablename__ = "units"

    unit_id = Column(Integer, primary_key=True)
    unit = Column(String(100), nullable=False)
    liquid = Column(Boolean, nullable=False)

    ingredientes = relationship("DB_Ingredient", back_populates="unit")


class DB_Ingredient(Base):
    __tablename__ = "ingredientes"

    ingredient_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), nullable=False)
    ingredient = Column(String(100), nullable=False)
    amount = Column(Float(2), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.unit_id"))

    recipe = relationship("DB_Recipe", back_populates="ingredientes")
    unit = relationship("DB_Unit", back_populates="ingredientes")
